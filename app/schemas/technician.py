"""
Technician Schemas
"""

from pydantic import BaseModel, Field, validator, EmailStr, condecimal
from typing import Optional
from datetime import datetime
from decimal import Decimal
import re


# Base Schema
class TechnicianBase(BaseModel):
    employee_id: str = Field(..., max_length=50, description="Unique employee ID")
    first_name: str = Field(..., max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    last_name: str = Field(..., max_length=100)
    
    specialization: str = Field(..., max_length=100)
    email: EmailStr = Field(...)
    phone: str = Field(..., max_length=20)
    
    @validator('specialization')
    def validate_specialization(cls, v):
        valid = [
            'lab', 'radiology', 'ecg', 'eeg', 'dialysis',
            'physiotherapy', 'pathology', 'blood_bank', 'microbiology',
            'biochemistry', 'ct_scan', 'mri', 'ultrasound', 'x_ray'
        ]
        if v.lower() not in valid:
            raise ValueError(f"Specialization must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validator('phone')
    def validate_phone(cls, v):
        if v and not re.match(r'^\+?1?\d{9,15}$', v.replace('-', '').replace(' ', '')):
            raise ValueError("Invalid phone number format")
        return v


# Create Schema
class TechnicianCreate(TechnicianBase):
    user_id: Optional[int] = None
    
    qualification: str = Field(..., max_length=200)
    license_number: Optional[str] = Field(None, max_length=100)
    license_expiry_date: Optional[str] = Field(None, max_length=20)
    
    years_of_experience: int = Field(default=0, ge=0)
    
    alternate_phone: Optional[str] = Field(None, max_length=20)
    
    address: str = Field(...)
    city: str = Field(..., max_length=100)
    state: str = Field(..., max_length=100)
    country: str = Field(default="USA", max_length=100)
    pincode: str = Field(..., max_length=20)
    
    department: str = Field(..., max_length=100)
    department_id: Optional[int] = None
    designation: Optional[str] = Field(None, max_length=100)
    
    joining_date: str = Field(..., max_length=20)
    leaving_date: Optional[str] = Field(None, max_length=20)
    shift: Optional[str] = Field(None, max_length=20)
    
    salary: Optional[condecimal(max_digits=12, decimal_places=2, gt=0)] = None
    salary_currency: str = Field(default="USD", max_length=3)
    
    is_available: bool = Field(default=True)
    is_on_duty: bool = Field(default=False)
    status: str = Field(default='active', max_length=20)
    
    skills: Optional[str] = Field(None, description="JSON array")
    certifications: Optional[str] = Field(None, description="JSON array")
    training_completed: Optional[str] = Field(None, description="JSON array")
    
    emergency_contact_name: Optional[str] = Field(None, max_length=200)
    emergency_contact_phone: Optional[str] = Field(None, max_length=20)
    emergency_contact_relation: Optional[str] = Field(None, max_length=50)
    
    languages_spoken: Optional[str] = Field(None, max_length=200)
    notes: Optional[str] = None
    profile_image: Optional[str] = Field(None, max_length=500)
    national_id: Optional[str] = Field(None, max_length=50)
    
    @validator('status')
    def validate_status(cls, v):
        valid = ['active', 'on_leave', 'resigned', 'terminated', 'retired', 'suspended']
        if v.lower() not in valid:
            raise ValueError(f"Status must be one of: {', '.join(valid)}")
        return v.lower()


# Update Schema
class TechnicianUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    
    specialization: Optional[str] = Field(None, max_length=100)
    qualification: Optional[str] = Field(None, max_length=200)
    license_number: Optional[str] = Field(None, max_length=100)
    license_expiry_date: Optional[str] = Field(None, max_length=20)
    
    years_of_experience: Optional[int] = Field(None, ge=0)
    
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    alternate_phone: Optional[str] = Field(None, max_length=20)
    
    address: Optional[str] = None
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    pincode: Optional[str] = Field(None, max_length=20)
    
    department: Optional[str] = Field(None, max_length=100)
    department_id: Optional[int] = None
    designation: Optional[str] = Field(None, max_length=100)
    
    leaving_date: Optional[str] = Field(None, max_length=20)
    shift: Optional[str] = Field(None, max_length=20)
    
    salary: Optional[condecimal(max_digits=12, decimal_places=2, gt=0)] = None
    
    is_available: Optional[bool] = None
    is_on_duty: Optional[bool] = None
    status: Optional[str] = Field(None, max_length=20)
    
    skills: Optional[str] = None
    certifications: Optional[str] = None
    training_completed: Optional[str] = None
    
    emergency_contact_name: Optional[str] = Field(None, max_length=200)
    emergency_contact_phone: Optional[str] = Field(None, max_length=20)
    emergency_contact_relation: Optional[str] = Field(None, max_length=50)
    
    languages_spoken: Optional[str] = Field(None, max_length=200)
    notes: Optional[str] = None
    profile_image: Optional[str] = Field(None, max_length=500)


# Response Schema
class TechnicianResponse(TechnicianBase):
    id: int
    user_id: Optional[int]
    
    qualification: str
    license_number: Optional[str]
    license_expiry_date: Optional[str]
    
    years_of_experience: int
    
    alternate_phone: Optional[str]
    
    address: str
    city: str
    state: str
    country: str
    pincode: str
    
    department: str
    department_id: Optional[int]
    designation: Optional[str]
    
    joining_date: str
    leaving_date: Optional[str]
    shift: Optional[str]
    
    salary: Optional[Decimal]
    salary_currency: str
    
    is_available: bool
    is_on_duty: bool
    status: str
    
    skills: Optional[str]
    certifications: Optional[str]
    training_completed: Optional[str]
    
    emergency_contact_name: Optional[str]
    emergency_contact_phone: Optional[str]
    emergency_contact_relation: Optional[str]
    
    languages_spoken: Optional[str]
    notes: Optional[str]
    profile_image: Optional[str]
    national_id: Optional[str]
    
    full_name: str
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v)
        }


# List Response
class TechnicianListResponse(BaseModel):
    total: int
    items: list[TechnicianResponse]
    page: int
    page_size: int
    total_pages: int