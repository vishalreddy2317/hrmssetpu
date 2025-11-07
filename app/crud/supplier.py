from app.crud.base import CRUDBase
from app.models.supplier import Supplier
from app.schemas.supplier import SupplierCreate, SupplierUpdate

supplier_crud = CRUDBase[Supplier, SupplierCreate, SupplierUpdate](Supplier)