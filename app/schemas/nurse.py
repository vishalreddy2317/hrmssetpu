"""
Nurse Schemas
"""

from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional
from datetime import datetime
import re


# Base Schema
class NurseBase(BaseModel):
    nurse_id: str = Field(..., max_length=20, description="Unique nurse ID")
    first_name: str = Field(..., max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    last_name: str = Field(..., max_length=100)
    
    qualification: str = Field(..., max_length=200)
    nursing_license_number: str = Field(..., max_length=100)
    
    email: EmailStr = Field(..., description="Email address")
    phone: str = Field(..., max_length=20)
    
    @validator('phone')
    def validate_phone(cls, v):
        if v and not re.match(r'^\+?1?\d{9,15}$', v.replace('-', '').replace(' ', '')):
            raise ValueError("Invalid phone number format")
        return v


# Create Schema
class NurseCreate(NurseBase):
    user_id: Optional[int] = None
    
    license_expiry_date: Optional[str] = Field(None, max_length=20)
    specialization: Optional[str] = Field(None, max_length=100)
    years_of_experience: int = Field(default=0, ge=0)
    
    alternate_phone: Optional[str] = Field(None, max_length=20)
    
    address: str = Field(...)
    city: str = Field(..., max_length=100)
    state: str = Field(..., max_length=100)
    country: str = Field(default="USA", max_length=100)
    pincode: str = Field(..., max_length=20)
    
    hospital_id: Optional[int] = None
    department_id: Optional[int] = None
    
    designation: Optional[str] = Field(None, max_length=100)
    employee_id: Optional[str] = Field(None, max_length=50)
    joining_date: Optional[str] = Field(None, max_length=20)
    shift: Optional[str] = Field(None, max_length=20)
    
    is_available: bool = Field(default=True)
    is_on_duty: bool = Field(default=False)
    status: str = Field(default='active', max_length=20)
    
    emergency_contact_name: Optional[str] = Field(None, max_length=200)
    emergency_contact_phone: Optional[str] = Field(None, max_length=20)
    
    certifications: Optional[str] = None
    languages_spoken: Optional[str] = Field(None, max_length=200)
    profile_image: Optional[str] = Field(None, max_length=500)
    
    @validator('status')
    def validate_status(cls, v):
        valid = ['active', 'on_leave', 'resigned', 'retired', 'suspended', 'inactive']
        if v.lower() not in valid:
            raise ValueError(f"Status must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validator('shift')
    def validate_shift(cls, v):
        if v:
            valid = ['morning', 'evening', 'night', 'rotating']
            if v.lower() not in valid:
                raise ValueError(f"Shift must be one of: {', '.join(valid)}")
            return v.lower()
        return v


# Update Schema
class NurseUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    
    qualification: Optional[str] = Field(None, max_length=200)
    nursing_license_number: Optional[str] = Field(None, max_length=100)
    license_expiry_date: Optional[str] = Field(None, max_length=20)
    specialization: Optional[str] = Field(None, max_length=100)
    years_of_experience: Optional[int] = Field(None, ge=0)
    
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    alternate_phone: Optional[str] = Field(None, max_length=20)
    
    address: Optional[str] = None
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    pincode: Optional[str] = Field(None, max_length=20)
    
    hospital_id: Optional[int] = None
    department_id: Optional[int] = None
    
    designation: Optional[str] = Field(None, max_length=100)
    shift: Optional[str] = Field(None, max_length=20)
    
    is_available: Optional[bool] = None
    is_on_duty: Optional[bool] = None
    status: Optional[str] = Field(None, max_length=20)
    
    emergency_contact_name: Optional[str] = Field(None, max_length=200)
    emergency_contact_phone: Optional[str] = Field(None, max_length=20)
    
    certifications: Optional[str] = None
    languages_spoken: Optional[str] = Field(None, max_length=200)
    profile_image: Optional[str] = Field(None, max_length=500)


# Response Schema
class NurseResponse(NurseBase):
    id: int
    user_id: Optional[int]
    
    license_expiry_date: Optional[str]
    specialization: Optional[str]
    years_of_experience: int
    
    alternate_phone: Optional[str]
    
    address: str
    city: str
    state: str
    country: str
    pincode: str
    
    hospital_id: Optional[int]
    department_id: Optional[int]
    
    designation: Optional[str]
    employee_id: Optional[str]
    joining_date: Optional[str]
    shift: Optional[str]
    
    is_available: bool
    is_on_duty: bool
    status: str
    
    emergency_contact_name: Optional[str]
    emergency_contact_phone: Optional[str]
    
    certifications: Optional[str]
    languages_spoken: Optional[str]
    profile_image: Optional[str]
    
    full_name: str
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# List Response
class NurseListResponse(BaseModel):
    total: int
    items: list[NurseResponse]
    page: int
    page_size: int
    total_pages: int


# Duty Status Update
class NurseDutyStatusUpdate(BaseModel):
    is_on_duty: bool = Field(..., description="Duty status")
    shift: Optional[str] = Field(None, max_length=20)


# Availability Update
class NurseAvailabilityUpdate(BaseModel):
    is_available: bool = Field(..., description="Availability status")
    reason: Optional[str] = Field(None, description="Reason for unavailability")