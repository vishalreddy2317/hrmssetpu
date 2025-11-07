from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.supplier import supplier_service

async def get_supplier_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await supplier_service.get_supplier(db, id=id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")
    return obj
