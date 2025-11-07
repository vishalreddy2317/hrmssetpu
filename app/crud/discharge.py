from app.crud.base import CRUDBase
from app.models.discharge import Discharge
from app.schemas.discharge import DischargeCreate, DischargeUpdate

discharge_crud = CRUDBase[Discharge, DischargeCreate, DischargeUpdate](Discharge)