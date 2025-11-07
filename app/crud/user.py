from app.crud.base import CRUDBase
from app.auth.models import User  # ✅ Import from auth
from app.schemas.user import UserCreate, UserUpdate

user_crud = CRUDBase[User, UserCreate, UserUpdate](User)