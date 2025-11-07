from app.crud.purchase_order import purchase_order_crud


class PurchaseOrderRepository:
    def __init__(self):
        self.crud = purchase_order_crud


purchase_order_repository = PurchaseOrderRepository()