from app.crud.base import CRUDBase
from app.models.doctor import Doctor
from app.schemas.doctor import DoctorCreate, DoctorUpdate

doctor_crud = CRUDBase[Doctor, DoctorCreate, DoctorUpdate](Doctor)