from app.crud.base import CRUDBase
from app.models.inventory import Inventory
from app.schemas.inventory import InventoryCreate, InventoryUpdate

inventory_crud = CRUDBase[Inventory, InventoryCreate, InventoryUpdate](Inventory)