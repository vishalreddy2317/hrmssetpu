from app.crud.transport import transport_crud


class TransportRepository:
    def __init__(self):
        self.crud = transport_crud


transport_repository = TransportRepository()