from app.crud.base import CRUDBase
from app.models.lab_report import LabReport
from app.schemas.lab_report import LabReportCreate, LabReportUpdate

lab_report_crud = CRUDBase[LabReport, LabReportCreate, LabReportUpdate](LabReport)