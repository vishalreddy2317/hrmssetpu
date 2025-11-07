from app.crud.base import CRUDBase
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate

patient_crud = CRUDBase[Patient, PatientCreate, PatientUpdate](Patient)