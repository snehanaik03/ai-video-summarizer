from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.summary import Summary
from app.schemas.summary import SummaryListResponse, SummaryResponse
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/api/notes", tags=["notes"])

@router.get("", response_model=SummaryListResponse)
@router.get("/", response_model=SummaryListResponse)
async def list_notes(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Summary)
        .where(Summary.user_id == current_user.id)
        .order_by(Summary.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    summaries = result.scalars().all()
    
    # Normally we'd do a count query for total, returning len for simplicity here
    return {"items": summaries, "total": len(summaries)}

@router.get("/{note_id}", response_model=SummaryResponse)
async def get_note(
    note_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Summary)
        .where(Summary.id == note_id, Summary.user_id == current_user.id)
    )
    note = result.scalar_one_or_none()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.delete("/{note_id}")
async def delete_note(
    note_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Summary)
        .where(Summary.id == note_id, Summary.user_id == current_user.id)
    )
    note = result.scalar_one_or_none()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
        
    await db.delete(note)
    await db.commit()
    return {"message": "Note deleted successfully"}
