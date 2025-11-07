from app.crud.chat import chat_crud


class ChatRepository:
    def __init__(self):
        self.crud = chat_crud


chat_repository = ChatRepository()