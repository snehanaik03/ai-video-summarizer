from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class MCQQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    correct_index: int
    explanation: str
    difficulty: str
    concept_tested: str

class QuizResponse(BaseModel):
    id: int
    summary_id: Optional[int] = None
    questions: List[MCQQuestion]
    created_at: datetime

class QuizSubmitRequest(BaseModel):
    answers: Dict[int, int]  # question_index -> selected_index

class QuestionResult(BaseModel):
    question_index: int
    is_correct: bool
    selected_index: int
    correct_index: int
    explanation: str

class QuizResultResponse(BaseModel):
    quiz_id: int
    score: float
    total: int
    percentage: float
    results: List[QuestionResult]
