from app.crud.base import CRUDBase
from app.models.setting import Setting
from app.schemas.setting import SettingCreate, SettingUpdate

setting_crud = CRUDBase[Setting, SettingCreate, SettingUpdate](Setting)