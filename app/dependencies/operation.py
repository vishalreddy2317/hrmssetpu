from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.operation import operation_service


async def get_operation_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await operation_service.get_operation(db, id=id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Operation not found"
        )
    return obj