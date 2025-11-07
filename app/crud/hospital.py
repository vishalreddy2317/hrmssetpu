from app.crud.base import CRUDBase
from app.models.hospital import Hospital
from app.schemas.hospital import HospitalCreate, HospitalUpdate

hospital_crud = CRUDBase[Hospital, HospitalCreate, HospitalUpdate](Hospital)