from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.ambulance import ambulance_service
from app.schemas.ambulance import AmbulanceCreate, AmbulanceUpdate
from app.dependencies.ambulance import get_ambulance_by_id

router = APIRouter(prefix="/ambulance", tags=["Ambulance"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_ambulance(data: AmbulanceCreate, db: AsyncSession = Depends(get_db)):
    return await ambulance_service.create_ambulance(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_ambulances(db: AsyncSession = Depends(get_db)):
    return await ambulance_service.list_ambulances(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_ambulance(obj = Depends(get_ambulance_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_ambulance(id: int, data: AmbulanceUpdate, db: AsyncSession = Depends(get_db)):
    return await ambulance_service.update_ambulance(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ambulance(id: int, db: AsyncSession = Depends(get_db)):
    return await ambulance_service.delete_ambulance(db, id)
