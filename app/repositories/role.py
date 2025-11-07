from app.crud.role import role_crud


class RoleRepository:
    def __init__(self):
        self.crud = role_crud


role_repository = RoleRepository()