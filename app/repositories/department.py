from app.crud.department import department_crud


class DepartmentRepository:
    def __init__(self):
        self.crud = department_crud


department_repository = DepartmentRepository()