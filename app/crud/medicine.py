from app.crud.base import CRUDBase
from app.models.medicine import Medicine
from app.schemas.medicine import MedicineCreate, MedicineUpdate

medicine_crud = CRUDBase[Medicine, MedicineCreate, MedicineUpdate](Medicine)