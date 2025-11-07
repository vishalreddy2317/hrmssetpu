from app.crud.base import CRUDBase
from app.models.insurance import Insurance
from app.schemas.insurance import InsuranceCreate, InsuranceUpdate

insurance_crud = CRUDBase[Insurance, InsuranceCreate, InsuranceUpdate](Insurance)