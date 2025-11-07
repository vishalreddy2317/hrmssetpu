from app.crud.stock import stock_crud


class StockRepository:
    def __init__(self):
        self.crud = stock_crud


stock_repository = StockRepository()