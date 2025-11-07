from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.test_result import test_result_service


async def get_test_result_by_id(id: int, db: AsyncSession = Depends(get_db)):
    obj = await test_result_service.get_test_result(db, id=id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Test result not found"
        )
    return obj