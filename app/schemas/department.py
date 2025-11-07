"""
Department Schemas - Pydantic V2
Department management with floor support
"""

from typing import Optional
from pydantic import Field, EmailStr, field_validator
from datetime import datetime

from .base import BaseSchema, BaseResponseSchema


# ============================================
# Department Create
# ============================================

class DepartmentCreate(BaseSchema):
    """Schema for creating department"""
    
    name: str = Field(..., min_length=2, max_length=100, description="Department name")
    code: str = Field(..., min_length=2, max_length=20, description="Unique department code")
    
    department_type: str = Field(
        ...,
        description="clinical, diagnostic, support, administrative"
    )
    
    # Floor Reference
    main_floor_id: Optional[int] = Field(default=None, description="Main floor ID")
    main_floor_number: Optional[int] = Field(default=None, ge=-10, le=100)
    
    # Location
    hospital_id: Optional[int] = None
    branch_id: Optional[int] = None
    building: Optional[str] = Field(default=None, max_length=50)
    wing: Optional[str] = Field(default=None, max_length=50)
    
    # Management
    head_doctor_id: Optional[int] = None
    contact_number: Optional[str] = Field(default=None, max_length=20)
    email: Optional[EmailStr] = None
    extension: Optional[str] = Field(default=None, max_length=10)
    
    # Capacity
    total_rooms: int = Field(default=0, ge=0)
    total_beds: int = Field(default=0, ge=0)
    
    # Status
    status: str = Field(default='active', max_length=20)
    is_emergency_department: bool = Field(default=False)
    is_24x7: bool = Field(default=False)
    
    # Additional
    description: Optional[str] = Field(default=None, max_length=1000)
    services_offered: Optional[str] = Field(default=None, max_length=2000)
    
    @field_validator('department_type')
    @classmethod
    def validate_department_type(cls, v: str) -> str:
        """Validate department type"""
        allowed = [
            'clinical', 'diagnostic', 'support', 'administrative',
            'emergency', 'surgical', 'medical', 'pediatric'
        ]
        if v.lower() not in allowed:
            raise ValueError(f'Department type must be one of: {", ".join(allowed)}')
        return v.lower()
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate status"""
        allowed = ['active', 'inactive', 'temporary_closed']
        if v.lower() not in allowed:
            raise ValueError(f'Status must be one of: {", ".join(allowed)}')
        return v.lower()


# ============================================
# Department Update
# ============================================

class DepartmentUpdate(BaseSchema):
    """Schema for updating department"""
    
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    main_floor_id: Optional[int] = None
    main_floor_number: Optional[int] = Field(default=None, ge=-10, le=100)
    contact_number: Optional[str] = Field(default=None, max_length=20)
    email: Optional[EmailStr] = None
    total_rooms: Optional[int] = Field(default=None, ge=0)
    total_beds: Optional[int] = Field(default=None, ge=0)
    status: Optional[str] = None
    description: Optional[str] = Field(default=None, max_length=1000)
    is_active: Optional[bool] = None


# ============================================
# Department Response
# ============================================

class DepartmentResponse(BaseResponseSchema):
    """Schema for department response"""
    
    name: str
    code: str
    department_type: str
    
    main_floor_id: Optional[int] = None
    main_floor_number: Optional[int] = None
    
    hospital_id: Optional[int] = None
    branch_id: Optional[int] = None
    building: Optional[str] = None
    wing: Optional[str] = None
    
    head_doctor_id: Optional[int] = None
    contact_number: Optional[str] = None
    email: Optional[str] = None
    
    total_doctors: int = 0
    total_nurses: int = 0
    total_staff: int = 0
    total_rooms: int
    total_beds: int
    
    status: str
    is_emergency_department: bool
    is_24x7: bool
    
    description: Optional[str] = None


class DepartmentDetailResponse(DepartmentResponse):
    """Detailed department response"""
    
    floor_name: Optional[str] = None
    head_doctor_name: Optional[str] = None
    rooms_count: int = 0
    wards_count: int = 0


# ============================================
# Exports
# ============================================

__all__ = [
    "DepartmentCreate",
    "DepartmentUpdate",
    "DepartmentResponse",
    "DepartmentDetailResponse",
]