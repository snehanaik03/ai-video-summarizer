import os
import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List

from app.database import get_db
from app.models.user import User
from app.models.summary import Summary
from app.models.quiz import Quiz
from app.schemas.summary import SummarizeRequest, SummaryResponse
from app.services.auth_service import get_optional_user, get_current_user
from app.services.youtube_service import youtube_service
from app.services.transcription_service import transcription_service
from app.services.ai_service import ai_service
from app.config import settings
from app.utils.exceptions import VideoSummarizerException, InvalidURLError

import asyncio
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

router = APIRouter(prefix="/api/summarize", tags=["summarize"])

class StreamSummarizeRequest(BaseModel):
    url: str
    processing_tier: str = "basic"

class TextSummarizeRequest(BaseModel):
    text: str
    tier: str = "basic"

@router.post("/youtube", response_model=List[SummaryResponse])
async def summarize_youtube(
    request: SummarizeRequest, 
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    results = []
    output_dir = settings.UPLOAD_DIR
    
    for url in request.urls:
        try:
            # 1. Non-blocking video extraction
            video_data = await asyncio.to_thread(youtube_service.process_youtube_url, url, output_dir)
            transcript = video_data["transcript"]
            
            # Transcribe if necessary
            if not transcript and video_data.get("audio_path"):
                audio_path = video_data["audio_path"]
                transcription_result = await asyncio.to_thread(
                    transcription_service.transcribe_audio,
                    audio_path,
                    request.separate_speaker
                )
                transcript = transcription_result["text"]
                if os.path.exists(audio_path):
                    os.remove(audio_path)
            
            if not transcript:
                raise HTTPException(status_code=400, detail=f"Could not get transcript for {url}")
                
            # 2. High-speed AI Summarization
            summary_result = await asyncio.to_thread(
                ai_service.summarize_transcript,
                transcript,
                request.processing_tier
            )
            
            # 3. High-speed Quiz Generation
            quiz_questions = await asyncio.to_thread(
                ai_service.generate_quiz,
                summary_result["detailed_summary"] or summary_result["summary"]
            )
            
            # 4. Asynchronous DB persistence
            new_summary = Summary(
                user_id=current_user.id if current_user else None,
                source_type="youtube",
                source_url=url,
                title=video_data["title"],
                thumbnail_url=video_data["thumbnail_url"],
                transcript=transcript,
                summary_text=summary_result["summary"],
                detailed_summary=summary_result["detailed_summary"],
                processing_tier=request.processing_tier
            )
            db.add(new_summary)
            await db.commit()
            await db.refresh(new_summary)
            
            new_quiz = Quiz(
                summary_id=new_summary.id,
                questions_json=json.dumps(quiz_questions)
            )
            db.add(new_quiz)
            await db.commit()
            
            results.append(new_summary)
            
        except VideoSummarizerException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to process video: {str(e)}")
            
    return results

@router.post("/youtube/stream")
async def summarize_youtube_stream(
    request: StreamSummarizeRequest,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    """
    Server-Sent Events (SSE) streaming endpoint.
    Streams summary tokens in real time to the frontend for instant responsiveness (<2s TTFT).
    """
    async def event_generator():
        output_dir = settings.UPLOAD_DIR
        try:
            # Step 1: Video extraction status
            yield f"data: {json.dumps({'type': 'status', 'step': 'extracting', 'message': 'Fetching video and captions...'})}\n\n"
            
            video_data = await asyncio.to_thread(youtube_service.process_youtube_url, request.url, output_dir)
            transcript = video_data.get("transcript")
            
            if not transcript and video_data.get("audio_path"):
                yield f"data: {json.dumps({'type': 'status', 'step': 'transcribing', 'message': 'Transcribing audio track with Whisper...'})}\n\n"
                audio_path = video_data["audio_path"]
                t_res = await asyncio.to_thread(transcription_service.transcribe_audio, audio_path)
                transcript = t_res["text"]
                if os.path.exists(audio_path):
                    os.remove(audio_path)
                    
            if not transcript:
                yield f"data: {json.dumps({'type': 'error', 'message': 'Could not extract transcript for video'})}\n\n"
                return

            yield f"data: {json.dumps({'type': 'metadata', 'title': video_data['title'], 'thumbnail_url': video_data.get('thumbnail_url')})}\n\n"
            yield f"data: {json.dumps({'type': 'status', 'step': 'generating', 'message': 'Synthesizing concise summary via Gemini Flash...'})}\n\n"
            
            # Step 2: Stream tokens chunk-by-chunk in real-time
            token_chunks = []
            for chunk in ai_service.summarize_transcript_stream(transcript, request.processing_tier):
                token_chunks.append(chunk)
                yield f"data: {json.dumps({'type': 'token', 'content': chunk})}\n\n"
                await asyncio.sleep(0.005)  # Yield to asyncio event loop
                
            full_summary = "".join(token_chunks)
            
            # Step 3: Quick Quiz generation
            yield f"data: {json.dumps({'type': 'status', 'step': 'quiz', 'message': 'Generating practice assessment questions...'})}\n\n"
            quiz_questions = await asyncio.to_thread(ai_service.generate_quiz, full_summary, 5)
            
            # Step 4: Persist in database
            new_summary = Summary(
                user_id=current_user.id if current_user else None,
                source_type="youtube",
                source_url=request.url,
                title=video_data["title"],
                thumbnail_url=video_data.get("thumbnail_url"),
                transcript=transcript,
                summary_text=full_summary,
                detailed_summary=full_summary,
                processing_tier=request.processing_tier
            )
            db.add(new_summary)
            await db.commit()
            await db.refresh(new_summary)
            
            new_quiz = Quiz(
                summary_id=new_summary.id,
                questions_json=json.dumps(quiz_questions)
            )
            db.add(new_quiz)
            await db.commit()
            
            # Step 5: Send completion payload
            yield f"data: {json.dumps({'type': 'complete', 'summary_id': new_summary.id, 'quiz': quiz_questions})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.post("/text", response_model=SummaryResponse)
async def summarize_text(
    request: TextSummarizeRequest,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    try:
        summary_result = ai_service.summarize_text(request.text, request.tier)
        quiz_questions = ai_service.generate_quiz(summary_result["detailed_summary"] or summary_result["summary"])
        
        new_summary = Summary(
            user_id=current_user.id if current_user else None,
            source_type="text",
            title="Text Summary",
            transcript=request.text,
            summary_text=summary_result["summary"],
            detailed_summary=summary_result["detailed_summary"],
            processing_tier=request.tier
        )
        db.add(new_summary)
        await db.commit()
        await db.refresh(new_summary)
        
        new_quiz = Quiz(
            summary_id=new_summary.id,
            questions_json=json.dumps(quiz_questions)
        )
        db.add(new_quiz)
        await db.commit()
        
        return new_summary
    except VideoSummarizerException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{summary_id}", response_model=SummaryResponse)
async def get_summary(summary_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Summary).where(Summary.id == summary_id))
    summary = result.scalar_one_or_none()
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary

@router.get("/history/list", response_model=List[SummaryResponse])
async def list_history(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Summary).where(Summary.user_id == current_user.id).order_by(Summary.created_at.desc()))
    return result.scalars().all()
