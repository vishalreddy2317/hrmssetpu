"""
Bed Schemas - Pydantic V2
Bed management and assignments
"""

from typing import Optional
from pydantic import Field, field_validator
from datetime import datetime
from decimal import Decimal

from .base import BaseSchema, BaseResponseSchema


# ============================================
# Bed Create
# ============================================

class BedCreate(BaseSchema):
    """Schema for creating bed"""
    
    bed_number: str = Field(..., min_length=1, max_length=20)
    bed_code: Optional[str] = Field(default=None, max_length=20)
    
    room_id: int = Field(..., description="Room ID where bed is located")
    ward_id: Optional[int] = None
    
    bed_type: str = Field(
        ...,
        description="general, icu, electric, manual, pediatric, maternity, bariatric"
    )
    
    # Specifications
    is_electric: bool = Field(default=False)
    has_side_rails: bool = Field(default=True)
    is_adjustable: bool = Field(default=False)
    weight_capacity_kg: Optional[Decimal] = Field(default=None, ge=0)
    
    # Equipment
    has_iv_stand: bool = Field(default=False)
    has_oxygen_port: bool = Field(default=False)
    has_suction_port: bool = Field(default=False)
    has_monitor: bool = Field(default=False)
    
    # Status
    status: str = Field(default='available', max_length=20)
    
    # Asset Management
    asset_tag: Optional[str] = Field(default=None, max_length=50)
    barcode: Optional[str] = Field(default=None, max_length=100)
    
    # Maintenance
    last_maintenance_date: Optional[str] = Field(default=None, max_length=20)
    next_maintenance_date: Optional[str] = Field(default=None, max_length=20)
    
    notes: Optional[str] = Field(default=None, max_length=500)
    
    @field_validator('bed_type')
    @classmethod
    def validate_bed_type(cls, v: str) -> str:
        """Validate bed type"""
        allowed = [
            'general', 'icu', 'electric', 'manual', 'pediatric',
            'maternity', 'bariatric', 'orthopedic', 'psychiatric'
        ]
        if v.lower() not in allowed:
            raise ValueError(f'Bed type must be one of: {", ".join(allowed)}')
        return v.lower()
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate status"""
        allowed = ['available', 'occupied', 'maintenance', 'reserved', 'cleaning', 'out_of_service']
        if v.lower() not in allowed:
            raise ValueError(f'Status must be one of: {", ".join(allowed)}')
        return v.lower()


# ============================================
# Bed Update
# ============================================

class BedUpdate(BaseSchema):
    """Schema for updating bed"""
    
    room_id: Optional[int] = None
    ward_id: Optional[int] = None
    status: Optional[str] = None
    is_available: Optional[bool] = None
    current_patient_id: Optional[int] = None
    last_maintenance_date: Optional[str] = Field(default=None, max_length=20)
    next_maintenance_date: Optional[str] = Field(default=None, max_length=20)
    notes: Optional[str] = Field(default=None, max_length=500)
    is_active: Optional[bool] = None


class BedAssignment(BaseSchema):
    """Schema for bed assignment"""
    
    bed_id: int = Field(..., description="Bed ID")
    patient_id: int = Field(..., description="Patient ID")
    notes: Optional[str] = Field(default=None, max_length=500)


class BedRelease(BaseSchema):
    """Schema for releasing bed"""
    
    bed_id: int = Field(..., description="Bed ID")
    notes: Optional[str] = Field(default=None, max_length=500)


# ============================================
# Bed Response
# ============================================

class BedResponse(BaseResponseSchema):
    """Schema for bed response"""
    
    bed_number: str
    bed_code: Optional[str] = None
    
    room_id: int
    ward_id: Optional[int] = None
    
    bed_type: str
    
    is_electric: bool
    has_side_rails: bool
    is_adjustable: bool
    weight_capacity_kg: Optional[Decimal] = None
    
    has_iv_stand: bool
    has_oxygen_port: bool
    has_suction_port: bool
    has_monitor: bool
    
    status: str
    is_available: bool
    
    current_patient_id: Optional[int] = None
    assigned_at: Optional[str] = None
    
    asset_tag: Optional[str] = None
    barcode: Optional[str] = None
    
    last_maintenance_date: Optional[str] = None
    next_maintenance_date: Optional[str] = None


class BedDetailResponse(BedResponse):
    """Detailed bed response"""
    
    room_number: Optional[str] = None
    ward_name: Optional[str] = None
    current_patient_name: Optional[str] = None
    floor_number: Optional[int] = None


# ============================================
# Exports
# ============================================

__all__ = [
    "BedCreate",
    "BedUpdate",
    "BedAssignment",
    "BedRelease",
    "BedResponse",
    "BedDetailResponse",
]