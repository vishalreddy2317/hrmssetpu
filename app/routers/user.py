from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.user import user_service
from app.schemas.user import UserCreate, UserUpdate
from app.dependencies.user import get_user_by_id

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await user_service.create_user(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_users(db: AsyncSession = Depends(get_db)):
    return await user_service.list_users(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_user(obj = Depends(get_user_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_user(id: int, data: UserUpdate, db: AsyncSession = Depends(get_db)):
    return await user_service.update_user(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, db: AsyncSession = Depends(get_db)):
    return await user_service.delete_user(db, id)
