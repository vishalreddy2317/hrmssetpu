from app.crud.ward import ward_crud


class WardRepository:
    def __init__(self):
        self.crud = ward_crud


ward_repository = WardRepository()