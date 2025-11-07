from app.crud.base import CRUDBase
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageUpdate

message_crud = CRUDBase[Message, MessageCreate, MessageUpdate](Message)