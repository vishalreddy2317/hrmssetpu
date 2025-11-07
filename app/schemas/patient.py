"""
Patient Schemas - Pydantic V2
Patient information and medical records
"""

from typing import Optional
from pydantic import Field, EmailStr, field_validator, model_validator
from datetime import datetime, date
from decimal import Decimal
import re

from .base import BaseSchema, BaseResponseSchema


# ============================================
# Patient Create
# ============================================

class PatientCreate(BaseSchema):
    """Schema for creating patient"""
    
    # Basic Information
    patient_id: str = Field(..., min_length=3, max_length=20, description="Unique patient ID")
    first_name: str = Field(..., min_length=2, max_length=100)
    middle_name: Optional[str] = Field(default=None, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    
    # Demographics
    date_of_birth: str = Field(..., description="Date of birth (YYYY-MM-DD)")
    age: int = Field(..., ge=0, le=150)
    gender: str = Field(..., description="male, female, other")
    
    # Contact
    email: Optional[EmailStr] = None
    phone: str = Field(..., min_length=10, max_length=20)
    alternate_phone: Optional[str] = Field(default=None, max_length=20)
    
    # Address
    address: str = Field(..., min_length=5, max_length=500)
    city: str = Field(..., min_length=2, max_length=100)
    state: str = Field(..., min_length=2, max_length=100)
    country: str = Field(default="USA", max_length=100)
    pincode: str = Field(..., min_length=3, max_length=20)
    
    # Emergency Contact
    emergency_contact_name: str = Field(..., min_length=2, max_length=200)
    emergency_contact_phone: str = Field(..., min_length=10, max_length=20)
    emergency_contact_relation: Optional[str] = Field(default=None, max_length=50)
    
    # Medical Information
    blood_group: Optional[str] = Field(default=None, max_length=5)
    height_cm: Optional[Decimal] = Field(default=None, ge=0, le=300)
    weight_kg: Optional[Decimal] = Field(default=None, ge=0, le=500)
    
    # Medical History
    allergies: Optional[str] = Field(default=None, max_length=2000)
    chronic_diseases: Optional[str] = Field(default=None, max_length=2000)
    current_medications: Optional[str] = Field(default=None, max_length=2000)
    medical_history: Optional[str] = Field(default=None, max_length=5000)
    family_medical_history: Optional[str] = Field(default=None, max_length=2000)
    
    # Hospital Assignment
    hospital_id: Optional[int] = None
    primary_doctor_id: Optional[int] = None
    
    # Insurance
    has_insurance: bool = Field(default=False)
    insurance_provider: Optional[str] = Field(default=None, max_length=200)
    insurance_policy_number: Optional[str] = Field(default=None, max_length=100)
    
    # Identification
    national_id: Optional[str] = Field(default=None, max_length=50)
    passport_number: Optional[str] = Field(default=None, max_length=50)
    
    # Additional Info
    occupation: Optional[str] = Field(default=None, max_length=100)
    marital_status: Optional[str] = Field(default=None, max_length=20)
    notes: Optional[str] = Field(default=None, max_length=2000)
    
    @field_validator('gender')
    @classmethod
    def validate_gender(cls, v: str) -> str:
        """Validate gender"""
        allowed = ['male', 'female', 'other']
        if v.lower() not in allowed:
            raise ValueError(f'Gender must be one of: {", ".join(allowed)}')
        return v.lower()
    
    @field_validator('blood_group')
    @classmethod
    def validate_blood_group(cls, v: Optional[str]) -> Optional[str]:
        """Validate blood group"""
        if v is None:
            return None
        allowed = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        if v.upper() not in allowed:
            raise ValueError(f'Blood group must be one of: {", ".join(allowed)}')
        return v.upper()
    
    @field_validator('phone', 'alternate_phone', 'emergency_contact_phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        """Validate phone number"""
        if v and len(v) < 10:
            raise ValueError("Phone number must be at least 10 digits")
        return v
    
    @field_validator('marital_status')
    @classmethod
    def validate_marital_status(cls, v: Optional[str]) -> Optional[str]:
        """Validate marital status"""
        if v is None:
            return None
        allowed = ['single', 'married', 'divorced', 'widowed']
        if v.lower() not in allowed:
            raise ValueError(f'Marital status must be one of: {", ".join(allowed)}')
        return v.lower()


# ============================================
# Patient Update
# ============================================

class PatientUpdate(BaseSchema):
    """Schema for updating patient"""
    
    first_name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    middle_name: Optional[str] = Field(default=None, max_length=100)
    last_name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, min_length=10, max_length=20)
    alternate_phone: Optional[str] = Field(default=None, max_length=20)
    
    address: Optional[str] = Field(default=None, min_length=5, max_length=500)
    city: Optional[str] = Field(default=None, max_length=100)
    state: Optional[str] = Field(default=None, max_length=100)
    pincode: Optional[str] = Field(default=None, max_length=20)
    
    emergency_contact_name: Optional[str] = Field(default=None, max_length=200)
    emergency_contact_phone: Optional[str] = Field(default=None, max_length=20)
    
    blood_group: Optional[str] = Field(default=None, max_length=5)
    height_cm: Optional[Decimal] = Field(default=None, ge=0, le=300)
    weight_kg: Optional[Decimal] = Field(default=None, ge=0, le=500)
    
    allergies: Optional[str] = Field(default=None, max_length=2000)
    chronic_diseases: Optional[str] = Field(default=None, max_length=2000)
    current_medications: Optional[str] = Field(default=None, max_length=2000)
    
    primary_doctor_id: Optional[int] = None
    
    insurance_provider: Optional[str] = Field(default=None, max_length=200)
    insurance_policy_number: Optional[str] = Field(default=None, max_length=100)
    
    occupation: Optional[str] = Field(default=None, max_length=100)
    marital_status: Optional[str] = Field(default=None, max_length=20)
    notes: Optional[str] = Field(default=None, max_length=2000)
    
    is_active: Optional[bool] = None


# ============================================
# Patient Response
# ============================================

class PatientResponse(BaseResponseSchema):
    """Schema for patient response"""
    
    patient_id: str
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    
    date_of_birth: str
    age: int
    gender: str
    
    email: Optional[str] = None
    phone: str
    alternate_phone: Optional[str] = None
    
    address: str
    city: str
    state: str
    country: str
    pincode: str
    
    emergency_contact_name: str
    emergency_contact_phone: str
    emergency_contact_relation: Optional[str] = None
    
    blood_group: Optional[str] = None
    height_cm: Optional[Decimal] = None
    weight_kg: Optional[Decimal] = None
    bmi: Optional[Decimal] = None
    
    allergies: Optional[str] = None
    chronic_diseases: Optional[str] = None
    current_medications: Optional[str] = None
    
    hospital_id: Optional[int] = None
    primary_doctor_id: Optional[int] = None
    
    current_bed_id: Optional[int] = None
    is_admitted: bool = False
    admission_date: Optional[str] = None
    
    has_insurance: bool
    insurance_provider: Optional[str] = None
    insurance_policy_number: Optional[str] = None
    
    national_id: Optional[str] = None
    
    status: str
    occupation: Optional[str] = None
    marital_status: Optional[str] = None
    
    @property
    def full_name(self) -> str:
        """Get full name"""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_address(self) -> str:
        """Get full formatted address"""
        return f"{self.address}, {self.city}, {self.state} {self.pincode}, {self.country}"


class PatientListResponse(BaseSchema):
    """Schema for patient list response"""
    
    id: int
    patient_id: str
    first_name: str
    last_name: str
    age: int
    gender: str
    phone: str
    is_admitted: bool
    status: str
    created_at: datetime


class PatientDetailResponse(PatientResponse):
    """Detailed patient response with related data"""
    
    primary_doctor_name: Optional[str] = None
    current_bed_number: Optional[str] = None
    current_room_number: Optional[str] = None
    appointments_count: int = 0
    admissions_count: int = 0
    total_billing: Decimal = Decimal('0.00')


# ============================================
# Exports
# ============================================

__all__ = [
    "PatientCreate",
    "PatientUpdate",
    "PatientResponse",
    "PatientListResponse",
    "PatientDetailResponse",
]