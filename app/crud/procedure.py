from app.crud.base import CRUDBase
from app.models.procedure import Procedure
from app.schemas.procedure import ProcedureCreate, ProcedureUpdate

procedure_crud = CRUDBase[Procedure, ProcedureCreate, ProcedureUpdate](Procedure)