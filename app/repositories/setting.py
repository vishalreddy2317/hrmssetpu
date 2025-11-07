from app.crud.setting import setting_crud


class SettingRepository:
    def __init__(self):
        self.crud = setting_crud


setting_repository = SettingRepository()