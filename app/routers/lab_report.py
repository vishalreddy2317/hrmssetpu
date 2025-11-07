from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.common import get_db
from app.services.lab_report import lab_report_service
from app.schemas.lab_report import LabReportCreate, LabReportUpdate
from app.dependencies.lab_report import get_lab_report_by_id

router = APIRouter(prefix="/lab_report", tags=["LabReport"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_lab_report(data: LabReportCreate, db: AsyncSession = Depends(get_db)):
    return await lab_report_service.create_lab_report(db, data)

@router.get("/", status_code=status.HTTP_200_OK)
async def list_lab_reports(db: AsyncSession = Depends(get_db)):
    return await lab_report_service.list_lab_reports(db)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_lab_report(obj = Depends(get_lab_report_by_id)):
    return obj

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_lab_report(id: int, data: LabReportUpdate, db: AsyncSession = Depends(get_db)):
    return await lab_report_service.update_lab_report(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lab_report(id: int, db: AsyncSession = Depends(get_db)):
    return await lab_report_service.delete_lab_report(db, id)
