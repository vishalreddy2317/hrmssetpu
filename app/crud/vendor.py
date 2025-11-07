from app.crud.base import CRUDBase
from app.models.vendor import Vendor
from app.schemas.vendor import VendorCreate, VendorUpdate

vendor_crud = CRUDBase[Vendor, VendorCreate, VendorUpdate](Vendor)