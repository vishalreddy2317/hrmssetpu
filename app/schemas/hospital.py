"""
Hospital Schemas - Pydantic V2
Hospital management and information
"""

from typing import Optional
from pydantic import Field, EmailStr, field_validator, ConfigDict
from datetime import datetime
from decimal import Decimal

from .base import BaseSchema, BaseResponseSchema


# ============================================
# Hospital Create
# ============================================

class HospitalCreate(BaseSchema):
    """Schema for creating hospital"""
    
    name: str = Field(..., min_length=2, max_length=200, description="Hospital name")
    code: str = Field(..., min_length=2, max_length=20, description="Unique hospital code")
    registration_number: Optional[str] = Field(default=None, max_length=100)
    
    hospital_type: str = Field(
        ...,
        description="general, specialized, clinic, multi_specialty, teaching, trauma_center"
    )
    
    # Location
    address: str = Field(..., min_length=5, max_length=500)
    city: str = Field(..., min_length=2, max_length=100)
    state: str = Field(..., min_length=2, max_length=100)
    country: str = Field(default="USA", max_length=100)
    pincode: str = Field(..., min_length=3, max_length=20)
    latitude: Optional[Decimal] = Field(default=None, ge=-90, le=90)
    longitude: Optional[Decimal] = Field(default=None, ge=-180, le=180)
    
    # Contact
    phone: Optional[str] = Field(default=None, max_length=20)
    email: Optional[EmailStr] = None
    website: Optional[str] = Field(default=None, max_length=200)
    emergency_phone: Optional[str] = Field(default=None, max_length=20)
    
    # Building Details
    total_floors: int = Field(default=1, ge=1, le=100)
    basement_floors: int = Field(default=0, ge=0, le=10)
    total_buildings: int = Field(default=1, ge=1)
    total_area_sqft: Optional[int] = Field(default=None, ge=0)
    
    # Capacity
    total_beds: int = Field(default=0, ge=0)
    total_rooms: int = Field(default=0, ge=0)
    total_wards: int = Field(default=0, ge=0)
    icu_beds: int = Field(default=0, ge=0)
    emergency_beds: int = Field(default=0, ge=0)
    operation_theaters: int = Field(default=0, ge=0)
    
    # Facilities
    has_emergency: bool = Field(default=True)
    has_ambulance: bool = Field(default=True)
    has_blood_bank: bool = Field(default=False)
    has_pharmacy: bool = Field(default=True)
    has_laboratory: bool = Field(default=True)
    has_radiology: bool = Field(default=True)
    has_icu: bool = Field(default=True)
    has_nicu: bool = Field(default=False)
    has_dialysis: bool = Field(default=False)
    has_mortuary: bool = Field(default=True)
    has_cafeteria: bool = Field(default=True)
    has_parking: bool = Field(default=True)
    
    # Accreditation
    accreditation: Optional[str] = Field(default=None, max_length=100)
    accreditation_body: Optional[str] = Field(default=None, max_length=100)
    license_number: Optional[str] = Field(default=None, max_length=100)
    license_expiry_date: Optional[str] = Field(default=None, max_length=20)
    
    # Status
    status: str = Field(default='active', max_length=20)
    is_24x7: bool = Field(default=True)
    is_government: bool = Field(default=False)
    
    # Additional
    description: Optional[str] = Field(default=None, max_length=2000)
    established_year: Optional[int] = Field(default=None, ge=1800, le=2100)
    specializations: Optional[str] = Field(default=None, max_length=1000)
    
    @field_validator('hospital_type')
    @classmethod
    def validate_hospital_type(cls, v: str) -> str:
        """Validate hospital type"""
        allowed = [
            'general', 'specialized', 'clinic', 'multi_specialty',
            'teaching', 'trauma_center', 'maternity', 'pediatric'
        ]
        if v.lower() not in allowed:
            raise ValueError(f'Hospital type must be one of: {", ".join(allowed)}')
        return v.lower()
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate status"""
        allowed = ['active', 'inactive', 'under_construction', 'temporary_closed']
        if v.lower() not in allowed:
            raise ValueError(f'Status must be one of: {", ".join(allowed)}')
        return v.lower()


# ============================================
# Hospital Update
# ============================================

class HospitalUpdate(BaseSchema):
    """Schema for updating hospital"""
    
    name: Optional[str] = Field(default=None, min_length=2, max_length=200)
    phone: Optional[str] = Field(default=None, max_length=20)
    email: Optional[EmailStr] = None
    website: Optional[str] = Field(default=None, max_length=200)
    emergency_phone: Optional[str] = Field(default=None, max_length=20)
    
    total_beds: Optional[int] = Field(default=None, ge=0)
    total_rooms: Optional[int] = Field(default=None, ge=0)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: Optional[str] = None
    is_active: Optional[bool] = None


# ============================================
# Hospital Response
# ============================================

class HospitalResponse(BaseResponseSchema):
    """Schema for hospital response"""
    
    name: str
    code: str
    registration_number: Optional[str] = None
    hospital_type: str
    
    address: str
    city: str
    state: str
    country: str
    pincode: str
    
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    emergency_phone: Optional[str] = None
    
    total_floors: int
    basement_floors: int
    total_buildings: int
    
    total_beds: int
    total_rooms: int
    total_wards: int
    icu_beds: int
    emergency_beds: int
    operation_theaters: int
    
    has_emergency: bool
    has_ambulance: bool
    has_blood_bank: bool
    has_pharmacy: bool
    has_laboratory: bool
    
    accreditation: Optional[str] = None
    license_number: Optional[str] = None
    
    status: str
    is_24x7: bool
    is_government: bool
    
    established_year: Optional[int] = None
    
    @property
    def full_address(self) -> str:
        """Get full formatted address"""
        return f"{self.address}, {self.city}, {self.state} {self.pincode}, {self.country}"
    
    @property
    def total_floor_count(self) -> int:
        """Total floors including basement"""
        return self.total_floors + self.basement_floors


class HospitalDetailResponse(HospitalResponse):
    """Detailed hospital response with statistics"""
    
    floors_count: int = 0
    departments_count: int = 0
    doctors_count: int = 0
    nurses_count: int = 0
    patients_count: int = 0
    occupancy_rate: float = 0.0


# ============================================
# Exports
# ============================================

__all__ = [
    "HospitalCreate",
    "HospitalUpdate",
    "HospitalResponse",
    "HospitalDetailResponse",
]