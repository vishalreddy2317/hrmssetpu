"""
Role Permission Schemas
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


# Base Schema
class RolePermissionBase(BaseModel):
    role_id: int = Field(..., gt=0)
    resource: str = Field(..., max_length=100, description="Resource name like patients, appointments")
    action: str = Field(..., max_length=50, description="Action like create, read, update, delete")
    
    @validator('action')
    def validate_action(cls, v):
        valid = ['create', 'read', 'update', 'delete', 'list', 'export', 'approve', 'reject', 'view']
        if v.lower() not in valid:
            raise ValueError(f"Action must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validator('resource')
    def validate_resource(cls, v):
        valid = [
            'patients', 'appointments', 'doctors', 'nurses', 'staff',
            'billing', 'payments', 'prescriptions', 'lab_tests', 'radiology',
            'pharmacy', 'inventory', 'departments', 'wards', 'beds',
            'admissions', 'discharges', 'procedures', 'reports', 'settings',
            'users', 'roles', 'permissions', 'audit_logs', 'notifications'
        ]
        if v.lower() not in valid:
            raise ValueError(f"Resource must be one of: {', '.join(valid)}")
        return v.lower()


# Create Schema
class RolePermissionCreate(RolePermissionBase):
    is_granted: bool = Field(default=True)
    conditions: Optional[str] = Field(None, max_length=500, description="JSON conditions")
    
    # permission_code will be auto-generated from resource:action


# Bulk Create Schema
class RolePermissionBulkCreate(BaseModel):
    role_id: int = Field(..., gt=0)
    permissions: list[dict] = Field(..., min_items=1, description="List of {resource, action, is_granted}")
    
    @validator('permissions')
    def validate_permissions(cls, v):
        for perm in v:
            if 'resource' not in perm or 'action' not in perm:
                raise ValueError("Each permission must have 'resource' and 'action'")
        return v


# Update Schema
class RolePermissionUpdate(BaseModel):
    is_granted: Optional[bool] = None
    conditions: Optional[str] = Field(None, max_length=500)


# Response Schema
class RolePermissionResponse(RolePermissionBase):
    id: int
    permission_code: str
    is_granted: bool
    conditions: Optional[str]
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# List Response
class RolePermissionListResponse(BaseModel):
    total: int
    items: list[RolePermissionResponse]
    page: int
    page_size: int
    total_pages: int


# Permission Template Schema
class PermissionTemplateSchema(BaseModel):
    template_name: str = Field(..., max_length=100, description="admin, doctor, nurse, patient, etc.")
    permissions: list[dict] = Field(..., description="List of {resource, action}")


# Check Permission Schema
class CheckPermissionSchema(BaseModel):
    role_id: int = Field(..., gt=0)
    resource: str = Field(..., max_length=100)
    action: str = Field(..., max_length=50)


# Check Permission Response
class CheckPermissionResponse(BaseModel):
    has_permission: bool
    permission_code: str
    conditions: Optional[str]
    message: Optional[str]


# Grant/Revoke Permission Schema
class GrantRevokePermissionSchema(BaseModel):
    resource: str = Field(..., max_length=100)
    action: str = Field(..., max_length=50)
    is_granted: bool = Field(...)
    conditions: Optional[str] = Field(None, max_length=500)


# Permission Summary Schema
class PermissionSummarySchema(BaseModel):
    role_id: int
    role_name: str
    total_permissions: int
    granted_permissions: int
    denied_permissions: int
    permissions_by_resource: dict  # {resource: count}
    permissions_by_action: dict  # {action: count}


# Available Permissions Schema
class AvailablePermissionsSchema(BaseModel):
    resources: list[str]
    actions: list[str]
    total_combinations: int
    permission_templates: list[str]


# Copy Permissions Schema
class CopyPermissionsSchema(BaseModel):
    from_role_id: int = Field(..., gt=0)
    to_role_id: int = Field(..., gt=0)
    overwrite_existing: bool = Field(default=False)
    
    @validator('to_role_id')
    def validate_different_roles(cls, v, values):
        if 'from_role_id' in values and v == values['from_role_id']:
            raise ValueError("Cannot copy permissions to the same role")
        return v


# Permission Matrix Response
class PermissionMatrixResponse(BaseModel):
    role_id: int
    role_name: str
    matrix: dict  # {resource: {action: is_granted}}
    
    class Config:
        json_encoders = {
            bool: lambda v: v
        }