from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SummarizeRequest(BaseModel):
    urls: List[str]
    processing_tier: str = "basic"
    separate_speaker: bool = False

class SummaryResponse(BaseModel):
    id: int
    user_id: Optional[int]
    source_type: str
    source_url: Optional[str]
    title: str
    thumbnail_url: Optional[str]
    transcript: str
    summary_text: str
    detailed_summary: Optional[str]
    processing_tier: str
    created_at: datetime

    class Config:
        from_attributes = True

class SummarizeUploadResponse(BaseModel):
    summary: SummaryResponse
    message: str

class SummaryListResponse(BaseModel):
    items: List[SummaryResponse]
    total: int
