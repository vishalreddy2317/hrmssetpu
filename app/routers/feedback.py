from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.feedback import feedback_service
from app.schemas.feedback import FeedbackCreate, FeedbackUpdate
from app.dependencies.feedback import get_feedback_by_id

router = APIRouter(prefix="/feedback", tags=["Feedback"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_feedback(data: FeedbackCreate, db: AsyncSession = Depends(get_db)):
    return await feedback_service.create_feedback(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_feedbacks(db: AsyncSession = Depends(get_db)):
    return await feedback_service.list_feedbacks(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_feedback(obj = Depends(get_feedback_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_feedback(id: int, data: FeedbackUpdate, db: AsyncSession = Depends(get_db)):
    return await feedback_service.update_feedback(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_feedback(id: int, db: AsyncSession = Depends(get_db)):
    return await feedback_service.delete_feedback(db, id)
