from app.crud.event import event_crud


class EventRepository:
    def __init__(self):
        self.crud = event_crud


event_repository = EventRepository()