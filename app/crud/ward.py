from app.crud.base import CRUDBase
from app.models.ward import Ward
from app.schemas.ward import WardCreate, WardUpdate

ward_crud = CRUDBase[Ward, WardCreate, WardUpdate](Ward)