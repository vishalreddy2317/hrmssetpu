from app.crud.base import CRUDBase
from app.models.revenue import Revenue
from app.schemas.revenue import RevenueCreate, RevenueUpdate

revenue_crud = CRUDBase[Revenue, RevenueCreate, RevenueUpdate](Revenue)