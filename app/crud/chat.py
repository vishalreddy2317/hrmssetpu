from app.crud.base import CRUDBase
from app.models.chat import Chat
from app.schemas.chat import ChatCreate, ChatUpdate

chat_crud = CRUDBase[Chat, ChatCreate, ChatUpdate](Chat)