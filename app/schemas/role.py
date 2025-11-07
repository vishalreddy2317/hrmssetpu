"""
Role Schemas
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


# Base Schema
class RoleBase(BaseModel):
    name: str = Field(..., max_length=100, description="Role name")
    code: str = Field(..., max_length=50, description="Unique role code")
    
    @validator('code')
    def validate_code(cls, v):
        # Code should be uppercase and use underscores
        if not v.isupper() or ' ' in v:
            raise ValueError("Code must be uppercase and use underscores instead of spaces")
        return v


# Create Schema
class RoleCreate(RoleBase):
    description: Optional[str] = None
    role_type: str = Field(default='custom', max_length=50)
    level: int = Field(default=0, ge=0, le=100, description="Higher = more privileges")
    status: str = Field(default='active', max_length=20)
    permissions: Optional[str] = Field(None, description="JSON array of permission codes")
    is_default_for: Optional[str] = Field(None, max_length=50)
    
    @validator('role_type')
    def validate_role_type(cls, v):
        valid = ['system', 'custom']
        if v.lower() not in valid:
            raise ValueError(f"Role type must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validator('status')
    def validate_status(cls, v):
        valid = ['active', 'inactive']
        if v.lower() not in valid:
            raise ValueError(f"Status must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validator('is_default_for')
    def validate_is_default_for(cls, v):
        if v:
            valid = ['doctor', 'nurse', 'patient', 'staff', 'admin', 'receptionist', 'pharmacist']
            if v.lower() not in valid:
                raise ValueError(f"Is default for must be one of: {', '.join(valid)}")
            return v.lower()
        return v


# Update Schema
class RoleUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    role_type: Optional[str] = Field(None, max_length=50)
    level: Optional[int] = Field(None, ge=0, le=100)
    status: Optional[str] = Field(None, max_length=20)
    permissions: Optional[str] = None
    is_default_for: Optional[str] = Field(None, max_length=50)


# Response Schema
class RoleResponse(RoleBase):
    id: int
    description: Optional[str]
    role_type: str
    level: int
    status: str
    permissions: Optional[str]
    is_default_for: Optional[str]
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# List Response
class RoleListResponse(BaseModel):
    total: int
    items: list[RoleResponse]
    page: int
    page_size: int
    total_pages: int


# Role with Permissions Response
class RoleWithPermissionsResponse(RoleResponse):
    permission_list: list["RolePermissionResponse"]
    permission_count: int
    
    class Config:
        from_attributes = True


# Assign Permissions Schema
class RoleAssignPermissionsSchema(BaseModel):
    permissions: list[str] = Field(..., min_items=1, description="List of permission codes")
    replace_existing: bool = Field(default=False, description="Replace or append to existing")


# Clone Role Schema
class RoleCloneSchema(BaseModel):
    new_name: str = Field(..., max_length=100)
    new_code: str = Field(..., max_length=50)
    include_permissions: bool = Field(default=True)
    description: Optional[str] = None