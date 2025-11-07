from app.crud.base import CRUDBase
from app.models.emergency import Emergency
from app.schemas.emergency import EmergencyCreate, EmergencyUpdate

emergency_crud = CRUDBase[Emergency, EmergencyCreate, EmergencyUpdate](Emergency)