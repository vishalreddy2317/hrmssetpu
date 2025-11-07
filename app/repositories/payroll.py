from app.crud.payroll import payroll_crud


class PayrollRepository:
    def __init__(self):
        self.crud = payroll_crud


payroll_repository = PayrollRepository()