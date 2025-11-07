from app.crud.base import CRUDBase
from app.models.branch import Branch
from app.schemas.branch import BranchCreate, BranchUpdate

branch_crud = CRUDBase[Branch, BranchCreate, BranchUpdate](Branch)