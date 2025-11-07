from app.crud.base import CRUDBase
from app.models.diagnosis import Diagnosis
from app.schemas.diagnosis import DiagnosisCreate, DiagnosisUpdate

diagnosis_crud = CRUDBase[Diagnosis, DiagnosisCreate, DiagnosisUpdate](Diagnosis)