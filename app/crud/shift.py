from app.crud.base import CRUDBase
from app.models.shift import Shift
from app.schemas.shift import ShiftCreate, ShiftUpdate

shift_crud = CRUDBase[Shift, ShiftCreate, ShiftUpdate](Shift)