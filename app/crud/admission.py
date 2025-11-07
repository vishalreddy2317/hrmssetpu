from app.crud.base import CRUDBase
from app.models.admission import Admission
from app.schemas.admission import AdmissionCreate, AdmissionUpdate

admission_crud = CRUDBase[Admission, AdmissionCreate, AdmissionUpdate](Admission)