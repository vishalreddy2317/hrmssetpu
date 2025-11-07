from app.crud.ambulance import ambulance_crud


class AmbulanceRepository:
    def __init__(self):
        self.crud = ambulance_crud


ambulance_repository = AmbulanceRepository()