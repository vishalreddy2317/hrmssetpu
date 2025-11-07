from app.crud.base import CRUDBase
from app.models.faq import FAQ
from app.schemas.faq import FAQCreate, FAQUpdate

faq_crud = CRUDBase[FAQ, FAQCreate, FAQUpdate](FAQ)