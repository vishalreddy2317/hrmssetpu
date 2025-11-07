from app.crud.base import CRUDBase
from app.models.transport import Transport
from app.schemas.transport import TransportCreate, TransportUpdate

transport_crud = CRUDBase[Transport, TransportCreate, TransportUpdate](Transport)