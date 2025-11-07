from app.crud.base import CRUDBase
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentUpdate

payment_crud = CRUDBase[Payment, PaymentCreate, PaymentUpdate](Payment)