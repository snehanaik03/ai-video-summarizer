import os
import json
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_db
from app.models.user import User
from app.models.summary import Summary
from app.models.quiz import Quiz
from app.schemas.summary import SummaryResponse
from app.services.auth_service import get_optional_user
from app.services.file_service import file_service
from app.services.transcription_service import transcription_service
from app.services.ai_service import ai_service
from app.config import settings

router = APIRouter(prefix="/api/upload", tags=["upload"])

async def process_file_and_create_summary(
    file_path: str, source_type: str, title: str, extract_func,
    db: AsyncSession, current_user: Optional[User]
) -> SummaryResponse:
    try:
        # 1. Extract Text/Transcript
        text = extract_func(file_path)
        
        # 2. Summarize
        summary_result = ai_service.summarize_transcript(text)
        
        # 3. Generate Quiz
        quiz_questions = ai_service.generate_quiz(summary_result["detailed_summary"] or summary_result["summary"])
        
        # 4. Save to DB
        new_summary = Summary(
            user_id=current_user.id if current_user else None,
            source_type=source_type,
            title=title,
            transcript=text,
            summary_text=summary_result["summary"],
            detailed_summary=summary_result["detailed_summary"]
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
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@router.post("/video", response_model=SummaryResponse)
async def upload_video(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    if not file_service.validate_file_type(file.filename, [".mp4", ".avi", ".mov", ".mkv"]):
        raise HTTPException(400, "Invalid video format")
        
    file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
    await file_service.save_upload_file(file, file_path)
    
    audio_path = None
    try:
        audio_path = file_service.extract_audio_from_video(file_path, settings.UPLOAD_DIR)
        
        def extract(f_path):
            return transcription_service.transcribe_audio(audio_path)["text"]
            
        return await process_file_and_create_summary(
            file_path, "video", file.filename, extract, db, current_user
        )
    finally:
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)
            
@router.post("/audio", response_model=SummaryResponse)
async def upload_audio(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    if not file_service.validate_file_type(file.filename, [".mp3", ".wav", ".m4a"]):
        raise HTTPException(400, "Invalid audio format")
        
    file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
    await file_service.save_upload_file(file, file_path)
    
    def extract(f_path):
        return transcription_service.transcribe_audio(f_path)["text"]
        
    return await process_file_and_create_summary(
        file_path, "audio", file.filename, extract, db, current_user
    )

@router.post("/pdf", response_model=SummaryResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    if not file_service.validate_file_type(file.filename, [".pdf"]):
        raise HTTPException(400, "Invalid PDF format")
        
    file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
    await file_service.save_upload_file(file, file_path)
    
    return await process_file_and_create_summary(
        file_path, "pdf", file.filename, file_service.extract_text_from_pdf, db, current_user
    )

@router.post("/image", response_model=SummaryResponse)
async def upload_image(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    if not file_service.validate_file_type(file.filename, [".jpg", ".jpeg", ".png"]):
        raise HTTPException(400, "Invalid image format")
        
    file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
    await file_service.save_upload_file(file, file_path)
    
    return await process_file_and_create_summary(
        file_path, "image", file.filename, file_service.extract_text_from_image, db, current_user
    )
