from app.crud.message import message_crud


class MessageRepository:
    def __init__(self):
        self.crud = message_crud


message_repository = MessageRepository()