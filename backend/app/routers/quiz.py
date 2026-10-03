import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models.user import User
from app.models.summary import Summary
from app.models.quiz import Quiz, QuizAttempt
from app.schemas.quiz import QuizResponse, QuizSubmitRequest, QuizResultResponse, QuestionResult, MCQQuestion
from app.services.auth_service import get_optional_user
from app.services.ai_service import ai_service

router = APIRouter(prefix="/api/quiz", tags=["quiz"])

@router.post("/generate/{summary_id}", response_model=QuizResponse)
async def generate_quiz_for_summary(
    summary_id: int, 
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Summary).where(Summary.id == summary_id))
    summary = result.scalar_one_or_none()
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    existing_result = await db.execute(select(Quiz).where(Quiz.summary_id == summary_id))
    existing_quiz = existing_result.scalar_one_or_none()
    if existing_quiz:
        return {
            "id": existing_quiz.id,
            "summary_id": existing_quiz.summary_id,
            "questions": json.loads(existing_quiz.questions_json),
            "created_at": existing_quiz.created_at
        }
        
    text_to_quiz = summary.detailed_summary if summary.detailed_summary else summary.summary_text
    
    quiz_questions = ai_service.generate_quiz(text_to_quiz)
    
    new_quiz = Quiz(
        summary_id=summary_id,
        questions_json=json.dumps(quiz_questions)
    )
    db.add(new_quiz)
    await db.commit()
    await db.refresh(new_quiz)
    
    return {
        "id": new_quiz.id,
        "summary_id": new_quiz.summary_id,
        "questions": quiz_questions,
        "created_at": new_quiz.created_at
    }

@router.get("/{quiz_id}", response_model=QuizResponse)
async def get_quiz(quiz_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Quiz).where(Quiz.id == quiz_id))
    quiz = result.scalar_one_or_none()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
        
    questions = json.loads(quiz.questions_json)
    return {
        "id": quiz.id,
        "summary_id": quiz.summary_id,
        "questions": questions,
        "created_at": quiz.created_at
    }

@router.post("/{quiz_id}/submit", response_model=QuizResultResponse)
async def submit_quiz(
    quiz_id: int, 
    request: QuizSubmitRequest, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_optional_user)
):
    result = await db.execute(select(Quiz).where(Quiz.id == quiz_id))
    quiz = result.scalar_one_or_none()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
        
    questions = json.loads(quiz.questions_json)
    total = len(questions)
    score = 0
    results = []
    
    for i, q in enumerate(questions):
        correct_index = q.get("correct_index")
        selected_index = request.answers.get(i, -1)
        is_correct = (selected_index == correct_index)
        if is_correct:
            score += 1
            
        results.append({
            "question_index": i,
            "is_correct": is_correct,
            "selected_index": selected_index,
            "correct_index": correct_index,
            "explanation": q.get("explanation")
        })
        
    attempt = QuizAttempt(
        quiz_id=quiz_id,
        user_id=current_user.id if current_user else None,
        answers_json=json.dumps(request.answers),
        score=score,
        total_questions=total
    )
    db.add(attempt)
    await db.commit()
    
    percentage = (score / total) * 100 if total > 0 else 0
    
    return {
        "quiz_id": quiz_id,
        "score": score,
        "total": total,
        "percentage": percentage,
        "results": results
    }
