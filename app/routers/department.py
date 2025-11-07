from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.department import department_service
from app.schemas.department import DepartmentCreate, DepartmentUpdate
from app.dependencies.department import get_department_by_id

router = APIRouter(prefix="/department", tags=["Department"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_department(data: DepartmentCreate, db: AsyncSession = Depends(get_db)):
    return await department_service.create_department(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_departments(db: AsyncSession = Depends(get_db)):
    return await department_service.list_departments(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_department(obj = Depends(get_department_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_department(id: int, data: DepartmentUpdate, db: AsyncSession = Depends(get_db)):
    return await department_service.update_department(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(id: int, db: AsyncSession = Depends(get_db)):
    return await department_service.delete_department(db, id)
