from app.crud.payment import payment_crud


class PaymentRepository:
    def __init__(self):
        self.crud = payment_crud


payment_repository = PaymentRepository()