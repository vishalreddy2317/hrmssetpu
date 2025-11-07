from app.crud.procedure import procedure_crud


class ProcedureRepository:
    def __init__(self):
        self.crud = procedure_crud


procedure_repository = ProcedureRepository()