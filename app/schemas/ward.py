"""
Ward Schemas - Pydantic V2
Ward management with floor support
"""

from typing import Optional
from pydantic import Field, field_validator
from datetime import datetime

from .base import BaseSchema, BaseResponseSchema


# ============================================
# Ward Create
# ============================================

class WardCreate(BaseSchema):
    """Schema for creating ward"""
    
    ward_name: str = Field(..., min_length=2, max_length=100)
    ward_code: str = Field(..., min_length=2, max_length=20)
    
    ward_type: str = Field(
        ...,
        description="general, icu, nicu, picu, pediatric, maternity, isolation"
    )
    
    # Floor Reference
    floor_id: Optional[int] = Field(default=None, description="Floor ID")
    floor_number: Optional[int] = Field(default=None, ge=-10, le=100)
    
    # Location
    department_id: Optional[int] = None
    building: Optional[str] = Field(default=None, max_length=50)
    wing: Optional[str] = Field(default=None, max_length=50)
    section: Optional[str] = Field(default=None, max_length=50)
    
    # Capacity
    total_beds: int = Field(default=0, ge=0)
    total_rooms: int = Field(default=0, ge=0)
    
    # Staff
    head_nurse_id: Optional[int] = None
    
    # Facilities
    has_isolation_room: bool = Field(default=False)
    has_emergency_equipment: bool = Field(default=True)
    has_nurse_station: bool = Field(default=True)
    has_waiting_area: bool = Field(default=True)
    has_oxygen_supply: bool = Field(default=True)
    has_ventilators: bool = Field(default=False)
    ventilator_count: int = Field(default=0, ge=0)
    
    # Contact
    contact_number: Optional[str] = Field(default=None, max_length=20)
    extension: Optional[str] = Field(default=None, max_length=10)
    
    # Status
    status: str = Field(default='active', max_length=20)
    
    # Additional
    description: Optional[str] = Field(default=None, max_length=1000)
    special_notes: Optional[str] = Field(default=None, max_length=1000)
    infection_control_level: Optional[str] = Field(default=None, max_length=20)
    
    @field_validator('ward_type')
    @classmethod
    def validate_ward_type(cls, v: str) -> str:
        """Validate ward type"""
        allowed = [
            'general', 'icu', 'nicu', 'picu', 'pediatric', 'maternity',
            'isolation', 'burns', 'cardiac', 'oncology', 'orthopedic'
        ]
        if v.lower() not in allowed:
            raise ValueError(f'Ward type must be one of: {", ".join(allowed)}')
        return v.lower()
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate status"""
        allowed = ['active', 'inactive', 'maintenance', 'under_renovation', 'closed']
        if v.lower() not in allowed:
            raise ValueError(f'Status must be one of: {", ".join(allowed)}')
        return v.lower()


# ============================================
# Ward Update
# ============================================

class WardUpdate(BaseSchema):
    """Schema for updating ward"""
    
    ward_name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    floor_id: Optional[int] = None
    floor_number: Optional[int] = Field(default=None, ge=-10, le=100)
    total_beds: Optional[int] = Field(default=None, ge=0)
    total_rooms: Optional[int] = Field(default=None, ge=0)
    head_nurse_id: Optional[int] = None
    ventilator_count: Optional[int] = Field(default=None, ge=0)
    contact_number: Optional[str] = Field(default=None, max_length=20)
    status: Optional[str] = None
    description: Optional[str] = Field(default=None, max_length=1000)
    is_active: Optional[bool] = None


# ============================================
# Ward Response
# ============================================

class WardResponse(BaseResponseSchema):
    """Schema for ward response"""
    
    ward_name: str
    ward_code: str
    ward_type: str
    
    floor_id: Optional[int] = None
    floor_number: Optional[int] = None
    
    department_id: Optional[int] = None
    building: Optional[str] = None
    wing: Optional[str] = None
    
    total_beds: int
    occupied_beds: int
    reserved_beds: int
    total_rooms: int
    
    head_nurse_id: Optional[int] = None
    total_nurses: int = 0
    
    has_isolation_room: bool
    has_emergency_equipment: bool
    has_oxygen_supply: bool
    has_ventilators: bool
    ventilator_count: int
    
    contact_number: Optional[str] = None
    status: str
    
    @property
    def available_beds(self) -> int:
        """Calculate available beds"""
        return max(0, self.total_beds - self.occupied_beds - self.reserved_beds)
    
    @property
    def occupancy_rate(self) -> float:
        """Calculate occupancy percentage"""
        if self.total_beds == 0:
            return 0.0
        return round((self.occupied_beds / self.total_beds) * 100, 2)


class WardDetailResponse(WardResponse):
    """Detailed ward response"""
    
    floor_name: Optional[str] = None
    department_name: Optional[str] = None
    head_nurse_name: Optional[str] = None
    rooms_list: list = []


# ============================================
# Exports
# ============================================

__all__ = [
    "WardCreate",
    "WardUpdate",
    "WardResponse",
    "WardDetailResponse",
]