from app.crud.vendor import vendor_crud


class VendorRepository:
    def __init__(self):
        self.crud = vendor_crud


vendor_repository = VendorRepository()