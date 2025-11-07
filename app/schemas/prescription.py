"""
Prescription Schemas
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


# Base Schema
class PrescriptionBase(BaseModel):
    prescription_number: str = Field(..., max_length=20, description="Unique prescription number")
    prescription_date: str = Field(..., max_length=20)
    patient_id: int = Field(..., gt=0)
    doctor_id: int = Field(..., gt=0)
    diagnosis: str = Field(..., description="Diagnosis")


# Create Schema
class PrescriptionCreate(PrescriptionBase):
    appointment_id: Optional[int] = None
    admission_id: Optional[int] = None
    
    symptoms: Optional[str] = None
    prescription_type: str = Field(default='outpatient', max_length=50)
    
    # Vital Signs
    temperature: Optional[str] = Field(None, max_length=10)
    blood_pressure: Optional[str] = Field(None, max_length=20)
    pulse_rate: Optional[str] = Field(None, max_length=10)
    respiratory_rate: Optional[str] = Field(None, max_length=10)
    
    # Instructions
    general_instructions: Optional[str] = None
    dietary_advice: Optional[str] = None
    precautions: Optional[str] = None
    
    # Follow-up
    follow_up_required: bool = Field(default=False)
    follow_up_date: Optional[str] = Field(None, max_length=20)
    follow_up_notes: Optional[str] = None
    
    lab_tests_recommended: Optional[str] = Field(None, description="JSON array")
    
    status: str = Field(default='active', max_length=20)
    valid_until: Optional[str] = Field(None, max_length=20)
    
    digital_signature: Optional[str] = Field(None, max_length=500)
    is_verified: bool = Field(default=False)
    
    is_dispensed: bool = Field(default=False)
    dispensed_by: Optional[str] = Field(None, max_length=100)
    dispensed_at: Optional[str] = Field(None, max_length=50)
    
    doctor_notes: Optional[str] = None
    pharmacy_notes: Optional[str] = None
    
    @validator('prescription_type')
    def validate_prescription_type(cls, v):
        valid = ['outpatient', 'inpatient', 'emergency', 'followup', 'discharge']
        if v.lower() not in valid:
            raise ValueError(f"Prescription type must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validator('status')
    def validate_status(cls, v):
        valid = ['active', 'completed', 'cancelled', 'expired', 'partially_dispensed']
        if v.lower() not in valid:
            raise ValueError(f"Status must be one of: {', '.join(valid)}")
        return v.lower()


# Update Schema
class PrescriptionUpdate(BaseModel):
    symptoms: Optional[str] = None
    prescription_type: Optional[str] = Field(None, max_length=50)
    
    temperature: Optional[str] = Field(None, max_length=10)
    blood_pressure: Optional[str] = Field(None, max_length=20)
    pulse_rate: Optional[str] = Field(None, max_length=10)
    respiratory_rate: Optional[str] = Field(None, max_length=10)
    
    general_instructions: Optional[str] = None
    dietary_advice: Optional[str] = None
    precautions: Optional[str] = None
    
    follow_up_required: Optional[bool] = None
    follow_up_date: Optional[str] = Field(None, max_length=20)
    follow_up_notes: Optional[str] = None
    
    lab_tests_recommended: Optional[str] = None
    
    status: Optional[str] = Field(None, max_length=20)
    valid_until: Optional[str] = Field(None, max_length=20)
    
    digital_signature: Optional[str] = Field(None, max_length=500)
    is_verified: Optional[bool] = None
    
    is_dispensed: Optional[bool] = None
    dispensed_by: Optional[str] = Field(None, max_length=100)
    dispensed_at: Optional[str] = Field(None, max_length=50)
    
    doctor_notes: Optional[str] = None
    pharmacy_notes: Optional[str] = None


# Response Schema
class PrescriptionResponse(PrescriptionBase):
    id: int
    appointment_id: Optional[int]
    admission_id: Optional[int]
    
    symptoms: Optional[str]
    prescription_type: str
    
    temperature: Optional[str]
    blood_pressure: Optional[str]
    pulse_rate: Optional[str]
    respiratory_rate: Optional[str]
    
    general_instructions: Optional[str]
    dietary_advice: Optional[str]
    precautions: Optional[str]
    
    follow_up_required: bool
    follow_up_date: Optional[str]
    follow_up_notes: Optional[str]
    
    lab_tests_recommended: Optional[str]
    
    status: str
    valid_until: Optional[str]
    
    digital_signature: Optional[str]
    is_verified: bool
    
    is_dispensed: bool
    dispensed_by: Optional[str]
    dispensed_at: Optional[str]
    
    doctor_notes: Optional[str]
    pharmacy_notes: Optional[str]
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# List Response
class PrescriptionListResponse(BaseModel):
    total: int
    items: list[PrescriptionResponse]
    page: int
    page_size: int
    total_pages: int


# Medicine Item Schema (for prescription)
class PrescriptionMedicineItem(BaseModel):
    medicine_id: int = Field(..., gt=0)
    dosage: str = Field(..., max_length=100)
    frequency: str = Field(..., max_length=100)
    duration: str = Field(..., max_length=50)
    quantity: int = Field(..., gt=0)
    instructions: Optional[str] = None


# Add Medicines Schema
class PrescriptionAddMedicinesSchema(BaseModel):
    medicines: list[PrescriptionMedicineItem] = Field(..., min_items=1)


# Dispense Schema
class PrescriptionDispenseSchema(BaseModel):
    dispensed_by: str = Field(..., max_length=100)
    dispensed_at: str = Field(..., max_length=50)
    pharmacy_notes: Optional[str] = None