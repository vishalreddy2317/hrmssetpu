from app.crud.supplier import supplier_crud


class SupplierRepository:
    def __init__(self):
        self.crud = supplier_crud


supplier_repository = SupplierRepository()