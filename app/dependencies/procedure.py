from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.procedure import procedure_service

async def get_procedure_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await procedure_service.get_procedure(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Procedure not found")
    return obj
