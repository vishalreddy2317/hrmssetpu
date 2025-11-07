from app.crud.base import CRUDBase
from app.models.medical_record import MedicalRecord
from app.schemas.medical_record import MedicalRecordCreate, MedicalRecordUpdate

medical_record_crud = CRUDBase[MedicalRecord, MedicalRecordCreate, MedicalRecordUpdate](MedicalRecord)