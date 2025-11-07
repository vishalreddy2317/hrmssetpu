"""
Appointment Schemas - Pydantic V2
Patient appointment scheduling
"""

from typing import Optional
from pydantic import Field, field_validator, model_validator
from datetime import datetime
from decimal import Decimal

from .base import BaseSchema, BaseResponseSchema


# ============================================
# Appointment Create
# ============================================

class AppointmentCreate(BaseSchema):
    """Schema for creating appointment"""
    
    # Required Fields
    appointment_date: str = Field(..., description="Date (YYYY-MM-DD)")
    appointment_time: str = Field(..., description="Time (HH:MM)")
    
    patient_id: int = Field(..., description="Patient ID")
    doctor_id: int = Field(..., description="Doctor ID")
    
    # Optional Fields
    department_id: Optional[int] = None
    
    appointment_type: str = Field(
        default='consultation',
        description="consultation, follow_up, emergency, routine_checkup, diagnostic, vaccination"
    )
    
    duration_minutes: int = Field(default=30, ge=5, le=240)
    
    reason: str = Field(..., min_length=5, max_length=2000)
    symptoms: Optional[str] = Field(default=None, max_length=2000)
    
    consultation_fee: Optional[Decimal] = Field(default=None, ge=0)
    
    @field_validator('appointment_type')
    @classmethod
    def validate_appointment_type(cls, v: str) -> str:
        """Validate appointment type"""
        allowed = [
            'consultation', 'follow_up', 'emergency', 'routine_checkup',
            'diagnostic', 'vaccination', 'therapy', 'counseling'
        ]
        if v.lower() not in allowed:
            raise ValueError(f'Appointment type must be one of: {", ".join(allowed)}')
        return v.lower()
    
    @field_validator('appointment_time')
    @classmethod
    def validate_time_format(cls, v: str) -> str:
        """Validate time format HH:MM"""
        import re
        if not re.match(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', v):
            raise ValueError("Time must be in HH:MM format (e.g., 14:30)")
        return v
    
    @field_validator('appointment_date')
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        """Validate date format YYYY-MM-DD"""
        import re
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', v):
            raise ValueError("Date must be in YYYY-MM-DD format")
        return v


# ============================================
# Appointment Update
# ============================================

class AppointmentUpdate(BaseSchema):
    """Schema for updating appointment"""
    
    appointment_date: Optional[str] = Field(default=None, description="Date (YYYY-MM-DD)")
    appointment_time: Optional[str] = Field(default=None, description="Time (HH:MM)")
    
    doctor_id: Optional[int] = None
    department_id: Optional[int] = None
    
    appointment_type: Optional[str] = None
    duration_minutes: Optional[int] = Field(default=None, ge=5, le=240)
    
    reason: Optional[str] = Field(default=None, max_length=2000)
    symptoms: Optional[str] = Field(default=None, max_length=2000)
    
    status: Optional[str] = None
    doctor_notes: Optional[str] = Field(default=None, max_length=2000)
    
    consultation_fee: Optional[Decimal] = Field(default=None, ge=0)
    payment_status: Optional[str] = None


class AppointmentCancel(BaseSchema):
    """Schema for canceling appointment"""
    
    appointment_id: int
    cancelled_by: str = Field(..., description="patient, doctor, admin")
    cancellation_reason: str = Field(..., min_length=5, max_length=500)


class AppointmentReschedule(BaseSchema):
    """Schema for rescheduling appointment"""
    
    appointment_id: int
    new_date: str = Field(..., description="New date (YYYY-MM-DD)")
    new_time: str = Field(..., description="New time (HH:MM)")
    reason: Optional[str] = Field(default=None, max_length=500)


# ============================================
# Appointment Response
# ============================================

class AppointmentResponse(BaseResponseSchema):
    """Schema for appointment response"""
    
    appointment_number: str
    appointment_date: str
    appointment_time: str
    
    patient_id: int
    doctor_id: int
    department_id: Optional[int] = None
    
    appointment_type: str
    duration_minutes: int
    
    reason: str
    symptoms: Optional[str] = None
    
    status: str
    
    doctor_notes: Optional[str] = None
    prescription_given: bool = False
    
    consultation_fee: Optional[Decimal] = None
    payment_status: str
    
    cancelled_by: Optional[str] = None
    cancellation_reason: Optional[str] = None
    cancelled_at: Optional[str] = None
    
    is_follow_up: bool = False
    parent_appointment_id: Optional[int] = None
    next_follow_up_date: Optional[str] = None
    
    checked_in_at: Optional[str] = None
    checked_out_at: Optional[str] = None


class AppointmentListResponse(BaseSchema):
    """Schema for appointment list response"""
    
    id: int
    appointment_number: str
    appointment_date: str
    appointment_time: str
    patient_id: int
    doctor_id: int
    appointment_type: str
    status: str
    payment_status: str
    created_at: datetime


class AppointmentDetailResponse(AppointmentResponse):
    """Detailed appointment response"""
    
    patient_name: str
    patient_phone: str
    patient_age: int
    
    doctor_name: str
    doctor_specialization: str
    department_name: Optional[str] = None
    
    prescription_id: Optional[int] = None
    billing_id: Optional[int] = None


# ============================================
# Exports
# ============================================

__all__ = [
    "AppointmentCreate",
    "AppointmentUpdate",
    "AppointmentCancel",
    "AppointmentReschedule",
    "AppointmentResponse",
    "AppointmentListResponse",
    "AppointmentDetailResponse",
]
