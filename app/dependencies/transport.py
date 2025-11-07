from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.transport import transport_service

async def get_transport_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await transport_service.get_transport(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transport not found")
    return obj
