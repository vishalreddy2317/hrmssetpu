from app.crud.base import CRUDBase
from app.models.operation import Operation
from app.schemas.operation import OperationCreate, OperationUpdate

operation_crud = CRUDBase[Operation, OperationCreate, OperationUpdate](Operation)