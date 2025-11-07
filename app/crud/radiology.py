from app.crud.base import CRUDBase
from app.models.radiology import Radiology
from app.schemas.radiology import RadiologyCreate, RadiologyUpdate

radiology_crud = CRUDBase[Radiology, RadiologyCreate, RadiologyUpdate](Radiology)