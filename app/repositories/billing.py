from app.crud.billing import billing_crud


class BillingRepository:
    def __init__(self):
        self.crud = billing_crud


billing_repository = BillingRepository()