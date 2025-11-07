from app.crud.bed import bed_crud


class BedRepository:
    def __init__(self):
        self.crud = bed_crud


bed_repository = BedRepository()