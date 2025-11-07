from app.crud.base import CRUDBase
from app.models.billing import Billing
from app.schemas.billing import BillingCreate, BillingUpdate

billing_crud = CRUDBase[Billing, BillingCreate, BillingUpdate](Billing)