from app.crud.base import CRUDBase
from app.models.purchase_order import PurchaseOrder
from app.schemas.purchase_order import PurchaseOrderCreate, PurchaseOrderUpdate

purchase_order_crud = CRUDBase[PurchaseOrder, PurchaseOrderCreate, PurchaseOrderUpdate](PurchaseOrder)