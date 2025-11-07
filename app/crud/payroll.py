from app.crud.base import CRUDBase
from app.models.payroll import Payroll
from app.schemas.payroll import PayrollCreate, PayrollUpdate

payroll_crud = CRUDBase[Payroll, PayrollCreate, PayrollUpdate](Payroll)