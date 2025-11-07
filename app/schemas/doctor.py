"""
Doctor Schemas - Pydantic V2
Medical staff and doctor profiles
"""

from typing import Optional
from pydantic import Field, EmailStr, field_validator
from datetime import datetime
from decimal import Decimal

from .base import BaseSchema, BaseResponseSchema


# ============================================
# Doctor Create
# ============================================

class DoctorCreate(BaseSchema):
    """Schema for creating doctor"""
    
    # User Reference
    user_id: Optional[int] = None
    
    # Basic Information
    doctor_id: str = Field(..., min_length=3, max_length=20)
    first_name: str = Field(..., min_length=2, max_length=100)
    middle_name: Optional[str] = Field(default=None, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    
    # Professional Information
    specialization: str = Field(..., min_length=2, max_length=100)
    qualification: str = Field(..., min_length=2, max_length=200)
    medical_license_number: str = Field(..., min_length=3, max_length=100)
    license_expiry_date: Optional[str] = Field(default=None, max_length=20)
    
    # Experience
    years_of_experience: int = Field(default=0, ge=0, le=70)
    previous_hospitals: Optional[str] = Field(default=None, max_length=1000)
    
    # Contact
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=20)
    alternate_phone: Optional[str] = Field(default=None, max_length=20)
    
    # Address
    address: str = Field(..., min_length=5, max_length=500)
    city: str = Field(..., min_length=2, max_length=100)
    state: str = Field(..., min_length=2, max_length=100)
    country: str = Field(default="USA", max_length=100)
    pincode: str = Field(..., min_length=3, max_length=20)
    
    # Hospital Assignment
    hospital_id: Optional[int] = None
    department_id: Optional[int] = None
    
    # Professional Details
    designation: Optional[str] = Field(default=None, max_length=100)
    employee_id: Optional[str] = Field(default=None, max_length=50)
    joining_date: Optional[str] = Field(default=None, max_length=20)
    
    # Consultation
    consultation_fee: Optional[Decimal] = Field(default=None, ge=0)
    average_consultation_time: int = Field(default=30, ge=5, le=240, description="Minutes")
    max_appointments_per_day: int = Field(default=20, ge=1, le=100)
    
    # Availability
    is_available: bool = Field(default=True)
    
    # Additional
    bio: Optional[str] = Field(default=None, max_length=2000)
    languages_spoken: Optional[str] = Field(default=None, max_length=200)
    awards_achievements: Optional[str] = Field(default=None, max_length=2000)
    research_publications: Optional[str] = Field(default=None, max_length=2000)
    
    @field_validator('phone', 'alternate_phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        """Validate phone number"""
        if v and len(v) < 10:
            raise ValueError("Phone number must be at least 10 digits")
        return v


# ============================================
# Doctor Update
# ============================================

class DoctorUpdate(BaseSchema):
    """Schema for updating doctor"""
    
    first_name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    middle_name: Optional[str] = Field(default=None, max_length=100)
    last_name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    
    phone: Optional[str] = Field(default=None, min_length=10, max_length=20)
    alternate_phone: Optional[str] = Field(default=None, max_length=20)
    email: Optional[EmailStr] = None
    
    address: Optional[str] = Field(default=None, max_length=500)
    city: Optional[str] = Field(default=None, max_length=100)
    state: Optional[str] = Field(default=None, max_length=100)
    pincode: Optional[str] = Field(default=None, max_length=20)
    
    department_id: Optional[int] = None
    designation: Optional[str] = Field(default=None, max_length=100)
    
    consultation_fee: Optional[Decimal] = Field(default=None, ge=0)
    average_consultation_time: Optional[int] = Field(default=None, ge=5, le=240)
    max_appointments_per_day: Optional[int] = Field(default=None, ge=1, le=100)
    
    is_available: Optional[bool] = None
    is_on_duty: Optional[bool] = None
    
    bio: Optional[str] = Field(default=None, max_length=2000)
    languages_spoken: Optional[str] = Field(default=None, max_length=200)
    
    status: Optional[str] = None
    is_active: Optional[bool] = None


# ============================================
# Doctor Response
# ============================================

class DoctorResponse(BaseResponseSchema):
    """Schema for doctor response"""
    
    user_id: Optional[int] = None
    
    doctor_id: str
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    
    specialization: str
    qualification: str
    medical_license_number: str
    license_expiry_date: Optional[str] = None
    
    years_of_experience: int
    
    email: str
    phone: str
    alternate_phone: Optional[str] = None
    
    address: str
    city: str
    state: str
    country: str
    pincode: str
    
    hospital_id: Optional[int] = None
    department_id: Optional[int] = None
    
    designation: Optional[str] = None
    employee_id: Optional[str] = None
    joining_date: Optional[str] = None
    
    consultation_fee: Optional[Decimal] = None
    average_consultation_time: int
    max_appointments_per_day: int
    
    is_available: bool
    is_on_duty: bool = False
    
    rating: Optional[Decimal] = None
    total_ratings: int = 0
    
    status: str
    
    bio: Optional[str] = None
    languages_spoken: Optional[str] = None
    profile_image: Optional[str] = None
    
    @property
    def full_name(self) -> str:
        """Get full name with title"""
        name = f"Dr. {self.first_name}"
        if self.middle_name:
            name += f" {self.middle_name}"
        name += f" {self.last_name}"
        return name
    
    @property
    def average_rating(self) -> float:
        """Get average rating"""
        if self.rating:
            return float(self.rating)
        return 0.0


class DoctorListResponse(BaseSchema):
    """Schema for doctor list response"""
    
    id: int
    doctor_id: str
    first_name: str
    last_name: str
    specialization: str
    department_id: Optional[int] = None
    consultation_fee: Optional[Decimal] = None
    rating: Optional[Decimal] = None
    is_available: bool
    status: str


class DoctorDetailResponse(DoctorResponse):
    """Detailed doctor response"""
    
    department_name: Optional[str] = None
    hospital_name: Optional[str] = None
    total_patients: int = 0
    total_appointments: int = 0
    completed_appointments: int = 0


# ============================================
# Exports
# ============================================

__all__ = [
    "DoctorCreate",
    "DoctorUpdate",
    "DoctorResponse",
    "DoctorListResponse",
    "DoctorDetailResponse",
]