"""
Floor Schemas - Pydantic V2
Building floor management
"""

from typing import Optional, List
from pydantic import Field, field_validator, model_validator, ConfigDict
from datetime import datetime

from .base import BaseSchema, BaseResponseSchema


# ============================================
# Floor Create
# ============================================

class FloorCreate(BaseSchema):
    """Schema for creating floor"""
    
    floor_number: int = Field(..., ge=-10, le=100, description="Floor number (0=ground, negative=basement)")
    floor_name: str = Field(..., min_length=1, max_length=100, description="Floor name")
    floor_code: Optional[str] = Field(default=None, max_length=20)
    
    hospital_id: Optional[int] = Field(default=None, description="Hospital ID")
    branch_id: Optional[int] = Field(default=None, description="Branch ID")
    
    total_rooms: int = Field(default=0, ge=0)
    total_wards: int = Field(default=0, ge=0)
    total_beds: int = Field(default=0, ge=0)
    
    square_footage: Optional[int] = Field(default=None, ge=0)
    description: Optional[str] = Field(default=None, max_length=1000)
    
    floor_type: Optional[str] = Field(
        default='general',
        description="general, icu, operation, emergency, administrative, diagnostic"
    )
    
    has_elevator: bool = Field(default=True)
    has_stairs: bool = Field(default=True)
    is_accessible: bool = Field(default=True, description="Wheelchair accessible")
    has_ramp: bool = Field(default=False)
    
    has_emergency_exit: bool = Field(default=True)
    fire_extinguishers_count: int = Field(default=0, ge=0)
    emergency_assembly_point: Optional[str] = Field(default=None, max_length=200)
    
    has_waiting_area: bool = Field(default=True)
    has_restroom: bool = Field(default=True)
    has_pantry: bool = Field(default=False)
    
    @field_validator('floor_number')
    @classmethod
    def validate_floor_number(cls, v: int) -> int:
        """Validate floor number range"""
        if v < -10 or v > 100:
            raise ValueError('Floor number must be between -10 and 100')
        return v
    
    @field_validator('floor_type')
    @classmethod
    def validate_floor_type(cls, v: Optional[str]) -> Optional[str]:
        """Validate floor type"""
        if v is None:
            return None
        
        allowed = [
            'general', 'icu', 'operation', 'emergency',
            'administrative', 'diagnostic', 'pharmacy', 'laboratory'
        ]
        if v.lower() not in allowed:
            raise ValueError(f'Floor type must be one of: {", ".join(allowed)}')
        return v.lower()
    
    @model_validator(mode='after')
    def validate_hospital_or_branch(self):
        """At least one of hospital_id or branch_id must be provided"""
        if not self.hospital_id and not self.branch_id:
            raise ValueError('Either hospital_id or branch_id must be provided')
        return self


# ============================================
# Floor Update
# ============================================

class FloorUpdate(BaseSchema):
    """Schema for updating floor"""
    
    floor_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    total_rooms: Optional[int] = Field(default=None, ge=0)
    total_wards: Optional[int] = Field(default=None, ge=0)
    total_beds: Optional[int] = Field(default=None, ge=0)
    square_footage: Optional[int] = Field(default=None, ge=0)
    description: Optional[str] = Field(default=None, max_length=1000)
    floor_type: Optional[str] = None
    has_elevator: Optional[bool] = None
    has_stairs: Optional[bool] = None
    is_accessible: Optional[bool] = None
    has_ramp: Optional[bool] = None
    has_emergency_exit: Optional[bool] = None
    fire_extinguishers_count: Optional[int] = Field(default=None, ge=0)
    is_active: Optional[bool] = None


# ============================================
# Floor Response
# ============================================

class FloorResponse(BaseResponseSchema):
    """Schema for floor response"""
    
    floor_number: int
    floor_name: str
    floor_code: Optional[str] = None
    
    hospital_id: Optional[int] = None
    branch_id: Optional[int] = None
    
    total_rooms: int
    total_wards: int
    total_beds: int
    occupied_beds: int
    
    square_footage: Optional[int] = None
    description: Optional[str] = None
    
    floor_type: Optional[str] = None
    
    has_elevator: bool
    has_stairs: bool
    is_accessible: bool
    has_ramp: bool
    
    has_emergency_exit: bool
    fire_extinguishers_count: int
    
    has_waiting_area: bool
    has_restroom: bool
    has_pantry: bool
    
    @property
    def display_name(self) -> str:
        """Get formatted floor display name"""
        if self.floor_number == 0:
            return "Ground Floor"
        elif self.floor_number < 0:
            return f"Basement {abs(self.floor_number)}"
        elif self.floor_number == 1:
            return "1st Floor"
        elif self.floor_number == 2:
            return "2nd Floor"
        elif self.floor_number == 3:
            return "3rd Floor"
        else:
            return f"{self.floor_number}th Floor"
    
    @property
    def available_beds(self) -> int:
        """Calculate available beds"""
        return max(0, self.total_beds - self.occupied_beds)
    
    @property
    def occupancy_rate(self) -> float:
        """Calculate occupancy percentage"""
        if self.total_beds == 0:
            return 0.0
        return round((self.occupied_beds / self.total_beds) * 100, 2)


class FloorListResponse(BaseSchema):
    """Schema for floor list response"""
    
    id: int
    floor_number: int
    floor_name: str
    floor_type: Optional[str] = None
    total_rooms: int
    total_beds: int
    occupied_beds: int
    is_active: bool
    
    @property
    def display_name(self) -> str:
        """Get formatted display name"""
        if self.floor_number == 0:
            return "Ground Floor"
        elif self.floor_number < 0:
            return f"Basement {abs(self.floor_number)}"
        return f"Floor {self.floor_number}"


class FloorDetailResponse(FloorResponse):
    """Detailed floor response with statistics"""
    
    rooms_count: int = 0
    wards_count: int = 0
    departments_count: int = 0
    equipment_count: int = 0


# ============================================
# Exports
# ============================================

__all__ = [
    "FloorCreate",
    "FloorUpdate",
    "FloorResponse",
    "FloorListResponse",
    "FloorDetailRespons",
]