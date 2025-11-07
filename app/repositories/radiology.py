from app.crud.radiology import radiology_crud


class RadiologyRepository:
    def __init__(self):
        self.crud = radiology_crud


radiology_repository = RadiologyRepository()