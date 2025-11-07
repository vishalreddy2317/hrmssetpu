from app.crud.base import CRUDBase
from app.models.technician import Technician
from app.schemas.technician import TechnicianCreate, TechnicianUpdate

technician_crud = CRUDBase[Technician, TechnicianCreate, TechnicianUpdate](Technician)