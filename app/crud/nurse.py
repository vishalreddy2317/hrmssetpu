from app.crud.base import CRUDBase
from app.models.nurse import Nurse
from app.schemas.nurse import NurseCreate, NurseUpdate

nurse_crud = CRUDBase[Nurse, NurseCreate, NurseUpdate](Nurse)