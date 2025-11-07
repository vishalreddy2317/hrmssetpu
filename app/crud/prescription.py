from app.crud.base import CRUDBase
from app.models.prescription import Prescription
from app.schemas.prescription import PrescriptionCreate, PrescriptionUpdate

prescription_crud = CRUDBase[Prescription, PrescriptionCreate, PrescriptionUpdate](Prescription)