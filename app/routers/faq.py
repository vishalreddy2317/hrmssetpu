from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.faq import faq_service
from app.schemas.faq import FAQCreate, FAQUpdate
from app.dependencies.faq import get_faq_by_id

router = APIRouter(prefix="/faq", tags=["Faq"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_faq(data: FAQCreate, db: AsyncSession = Depends(get_db)):
    return await faq_service.create_faq(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_faqs(db: AsyncSession = Depends(get_db)):
    return await faq_service.list_faqs(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_faq(obj = Depends(get_faq_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_faq(id: int, data: FAQUpdate, db: AsyncSession = Depends(get_db)):
    return await faq_service.update_faq(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_faq(id: int, db: AsyncSession = Depends(get_db)):
    return await faq_service.delete_faq(db, id)
