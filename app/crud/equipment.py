from app.crud.base import CRUDBase
from app.models.equipment import Equipment
from app.schemas.equipment import EquipmentCreate, EquipmentUpdate

equipment_crud = CRUDBase[Equipment, EquipmentCreate, EquipmentUpdate](Equipment)