from app.crud.base import CRUDBase
from app.models.role_permission import RolePermission
from app.schemas.role_permission import RolePermissionCreate, RolePermissionUpdate

role_permission_crud = CRUDBase[RolePermission, RolePermissionCreate, RolePermissionUpdate](RolePermission)