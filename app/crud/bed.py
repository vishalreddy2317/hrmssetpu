from app.crud.base import CRUDBase
from app.models.bed import Bed
from app.schemas.bed import BedCreate, BedUpdate

bed_crud = CRUDBase[Bed, BedCreate, BedUpdate](Bed)