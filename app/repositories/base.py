from app.crud.base import CRUDBase
from app.models.base import Base

# ✅ Generic base repository using dict placeholders
base_crud = CRUDBase[Base, dict, dict](Base)


class BaseRepository:
    def __init__(self):
        self.crud = base_crud


base_repository = BaseRepository()