from app.crud.base import CRUDBase
from app.models.api_key import APIKey
from app.schemas.api_key import APIKeyCreate, APIKeyUpdate

api_key_crud = CRUDBase[APIKey, APIKeyCreate, APIKeyUpdate](APIKey)