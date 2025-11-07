from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.transport import transport_service
from app.schemas.transport import TransportCreate, TransportUpdate
from app.dependencies.transport import get_transport_by_id

router = APIRouter(prefix="/transport", tags=["Transport"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_transport(data: TransportCreate, db: AsyncSession = Depends(get_db)):
    return await transport_service.create_transport(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_transports(db: AsyncSession = Depends(get_db)):
    return await transport_service.list_transports(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_transport(obj = Depends(get_transport_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_transport(id: int, data: TransportUpdate, db: AsyncSession = Depends(get_db)):
    return await transport_service.update_transport(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transport(id: int, db: AsyncSession = Depends(get_db)):
    return await transport_service.delete_transport(db, id)
