from app.crud.base import CRUDBase
from app.models.ambulance import Ambulance
from app.schemas.ambulance import AmbulanceCreate, AmbulanceUpdate

ambulance_crud = CRUDBase[Ambulance, AmbulanceCreate, AmbulanceUpdate](Ambulance)