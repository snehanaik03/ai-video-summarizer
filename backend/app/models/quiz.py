from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    summary_id = Column(Integer, ForeignKey("summaries.id"))
    questions_json = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    summary = relationship("Summary", back_populates="quiz")
    attempts = relationship("QuizAttempt", back_populates="quiz")

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    answers_json = Column(Text)
    score = Column(Float)
    total_questions = Column(Integer)
    attempted_at = Column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    quiz = relationship("Quiz", back_populates="attempts")
    user = relationship("User", back_populates="quiz_attempts")
