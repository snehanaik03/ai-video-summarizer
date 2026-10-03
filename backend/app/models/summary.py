from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class Summary(Base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    source_type = Column(String)
    source_url = Column(String, nullable=True)
    title = Column(String)
    thumbnail_url = Column(String, nullable=True)
    transcript = Column(Text)
    summary_text = Column(Text)
    detailed_summary = Column(Text, nullable=True)
    processing_tier = Column(String, default="basic")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    user = relationship("User", back_populates="summaries")
    quiz = relationship("Quiz", back_populates="summary", uselist=False)
