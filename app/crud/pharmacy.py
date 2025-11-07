from app.crud.base import CRUDBase
from app.models.pharmacy import Pharmacy
from app.schemas.pharmacy import PharmacyCreate, PharmacyUpdate

pharmacy_crud = CRUDBase[Pharmacy, PharmacyCreate, PharmacyUpdate](Pharmacy)