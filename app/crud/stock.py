from app.crud.base import CRUDBase
from app.models.stock import Stock
from app.schemas.stock import StockCreate, StockUpdate

stock_crud = CRUDBase[Stock, StockCreate, StockUpdate](Stock)