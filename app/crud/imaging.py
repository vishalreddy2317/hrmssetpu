from app.crud.base import CRUDBase
from app.models.imaging import Imaging
from app.schemas.imaging import ImagingCreate, ImagingUpdate

imaging_crud = CRUDBase[Imaging, ImagingCreate, ImagingUpdate](Imaging)