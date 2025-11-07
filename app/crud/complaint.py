from app.crud.base import CRUDBase
from app.models.complaint import Complaint
from app.schemas.complaint import ComplaintCreate, ComplaintUpdate

complaint_crud = CRUDBase[Complaint, ComplaintCreate, ComplaintUpdate](Complaint)