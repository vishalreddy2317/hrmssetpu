from app.crud.base import CRUDBase
from app.models.vaccine import Vaccine
from app.schemas.vaccine import VaccineCreate, VaccineUpdate

vaccine_crud = CRUDBase[Vaccine, VaccineCreate, VaccineUpdate](Vaccine)