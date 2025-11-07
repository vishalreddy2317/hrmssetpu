from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.lab_test import lab_test_service
from app.schemas.lab_test import LabTestCreate, LabTestUpdate
from app.dependencies.lab_test import get_lab_test_by_id

router = APIRouter(prefix="/lab_test", tags=["LabTest"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_lab_test(data: LabTestCreate, db: AsyncSession = Depends(get_db)):
    return await lab_test_service.create_lab_test(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_lab_tests(db: AsyncSession = Depends(get_db)):
    return await lab_test_service.list_lab_tests(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_lab_test(obj = Depends(get_lab_test_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_lab_test(id: int, data: LabTestUpdate, db: AsyncSession = Depends(get_db)):
    return await lab_test_service.update_lab_test(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lab_test(id: int, db: AsyncSession = Depends(get_db)):
    return await lab_test_service.delete_lab_test(db, id)
