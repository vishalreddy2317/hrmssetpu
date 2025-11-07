from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.procedure import procedure_service
from app.schemas.procedure import ProcedureCreate, ProcedureUpdate
from app.dependencies.procedure import get_procedure_by_id

router = APIRouter(prefix="/procedure", tags=["Procedure"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_procedure(data: ProcedureCreate, db: AsyncSession = Depends(get_db)):
    return await procedure_service.create_procedure(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_procedures(db: AsyncSession = Depends(get_db)):
    return await procedure_service.list_procedures(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_procedure(obj = Depends(get_procedure_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_procedure(id: int, data: ProcedureUpdate, db: AsyncSession = Depends(get_db)):
    return await procedure_service.update_procedure(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_procedure(id: int, db: AsyncSession = Depends(get_db)):
    return await procedure_service.delete_procedure(db, id)
