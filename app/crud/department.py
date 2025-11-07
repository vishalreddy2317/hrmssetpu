from app.crud.base import CRUDBase
from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentUpdate

department_crud = CRUDBase[Department, DepartmentCreate, DepartmentUpdate](Department)