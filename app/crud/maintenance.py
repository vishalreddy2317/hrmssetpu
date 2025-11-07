from app.crud.base import CRUDBase
from app.models.maintenance import Maintenance
from app.schemas.maintenance import MaintenanceCreate, MaintenanceUpdate

maintenance_crud = CRUDBase[Maintenance, MaintenanceCreate, MaintenanceUpdate](Maintenance)