from app.crud.base import CRUDBase
from app.models.room import Room
from app.schemas.room import RoomCreate, RoomUpdate

room_crud = CRUDBase[Room, RoomCreate, RoomUpdate](Room)