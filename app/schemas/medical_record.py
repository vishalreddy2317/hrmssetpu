"""
Medical Record Schemas
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


# Base Schema
class MedicalRecordBase(BaseModel):
    record_number: str = Field(..., max_length=20, description="Unique record number")
    patient_id: int = Field(..., gt=0)
    record_type: str = Field(default='general', max_length=50)
    
    @validator('record_type')
    def validate_record_type(cls, v):
        valid = ['general', 'consultation', 'emergency', 'follow_up', 'discharge', 'admission']
        if v.lower() not in valid:
            raise ValueError(f"Record type must be one of: {', '.join(valid)}")
        return v.lower()


# Create Schema
class MedicalRecordCreate(MedicalRecordBase):
    doctor_id: Optional[int] = None
    appointment_id: Optional[int] = None
    diagnosis_id: Optional[int] = None
    
    visit_date: str = Field(..., max_length=20)
    visit_time: Optional[str] = Field(None, max_length=10)
    
    # Chief Complaint
    chief_complaint: Optional[str] = None
    
    # Vital Signs
    temperature: Optional[str] = Field(None, max_length=10)
    blood_pressure: Optional[str] = Field(None, max_length=20)
    pulse_rate: Optional[str] = Field(None, max_length=10)
    respiratory_rate: Optional[str] = Field(None, max_length=10)
    oxygen_saturation: Optional[str] = Field(None, max_length=10)
    weight: Optional[str] = Field(None, max_length=10)
    height: Optional[str] = Field(None, max_length=10)
    bmi: Optional[str] = Field(None, max_length=10)
    
    # Clinical Notes
    history_of_present_illness: Optional[str] = None
    past_medical_history: Optional[str] = None
    family_history: Optional[str] = None
    social_history: Optional[str] = None
    
    # Physical Examination
    physical_examination: Optional[str] = None
    
    # Assessment and Plan
    assessment: Optional[str] = None
    diagnosis_notes: Optional[str] = None
    treatment_plan: Optional[str] = None
    
    # Medications
    medications_prescribed: Optional[str] = Field(None, description="JSON array")
    
    # Tests
    lab_tests_ordered: Optional[str] = Field(None, description="JSON array")
    imaging_ordered: Optional[str] = Field(None, description="JSON array")
    
    # Procedures
    procedures_performed: Optional[str] = None
    
    # Follow-up
    follow_up_required: bool = Field(default=False)
    follow_up_date: Optional[str] = Field(None, max_length=20)
    follow_up_instructions: Optional[str] = None
    
    # Discharge
    discharge_summary: Optional[str] = None
    discharge_date: Optional[str] = Field(None, max_length=20)
    discharge_instructions: Optional[str] = None
    
    # Allergies
    allergies: Optional[str] = Field(None, description="JSON array")
    alerts: Optional[str] = None
    
    # Documents
    attachments: Optional[str] = Field(None, description="JSON array")
    
    # Notes
    notes: Optional[str] = None
    doctor_notes: Optional[str] = None
    nurse_notes: Optional[str] = None
    
    status: str = Field(default='active', max_length=20)
    is_confidential: bool = Field(default=False)


# Update Schema
class MedicalRecordUpdate(BaseModel):
    doctor_id: Optional[int] = None
    diagnosis_id: Optional[int] = None
    record_type: Optional[str] = Field(None, max_length=50)
    
    visit_time: Optional[str] = Field(None, max_length=10)
    chief_complaint: Optional[str] = None
    
    # Vital Signs
    temperature: Optional[str] = Field(None, max_length=10)
    blood_pressure: Optional[str] = Field(None, max_length=20)
    pulse_rate: Optional[str] = Field(None, max_length=10)
    respiratory_rate: Optional[str] = Field(None, max_length=10)
    oxygen_saturation: Optional[str] = Field(None, max_length=10)
    weight: Optional[str] = Field(None, max_length=10)
    height: Optional[str] = Field(None, max_length=10)
    bmi: Optional[str] = Field(None, max_length=10)
    
    # Clinical Notes
    history_of_present_illness: Optional[str] = None
    past_medical_history: Optional[str] = None
    family_history: Optional[str] = None
    social_history: Optional[str] = None
    
    physical_examination: Optional[str] = None
    assessment: Optional[str] = None
    diagnosis_notes: Optional[str] = None
    treatment_plan: Optional[str] = None
    
    medications_prescribed: Optional[str] = None
    lab_tests_ordered: Optional[str] = None
    imaging_ordered: Optional[str] = None
    procedures_performed: Optional[str] = None
    
    follow_up_required: Optional[bool] = None
    follow_up_date: Optional[str] = Field(None, max_length=20)
    follow_up_instructions: Optional[str] = None
    
    discharge_summary: Optional[str] = None
    discharge_date: Optional[str] = Field(None, max_length=20)
    discharge_instructions: Optional[str] = None
    
    allergies: Optional[str] = None
    alerts: Optional[str] = None
    attachments: Optional[str] = None
    
    notes: Optional[str] = None
    doctor_notes: Optional[str] = None
    nurse_notes: Optional[str] = None
    
    status: Optional[str] = Field(None, max_length=20)
    is_confidential: Optional[bool] = None


# Response Schema
class MedicalRecordResponse(MedicalRecordBase):
    id: int
    doctor_id: Optional[int]
    appointment_id: Optional[int]
    diagnosis_id: Optional[int]
    
    visit_date: str
    visit_time: Optional[str]
    chief_complaint: Optional[str]
    
    # Vital Signs
    temperature: Optional[str]
    blood_pressure: Optional[str]
    pulse_rate: Optional[str]
    respiratory_rate: Optional[str]
    oxygen_saturation: Optional[str]
    weight: Optional[str]
    height: Optional[str]
    bmi: Optional[str]
    
    # Clinical Notes
    history_of_present_illness: Optional[str]
    past_medical_history: Optional[str]
    family_history: Optional[str]
    social_history: Optional[str]
    
    physical_examination: Optional[str]
    assessment: Optional[str]
    diagnosis_notes: Optional[str]
    treatment_plan: Optional[str]
    
    medications_prescribed: Optional[str]
    lab_tests_ordered: Optional[str]
    imaging_ordered: Optional[str]
    procedures_performed: Optional[str]
    
    follow_up_required: bool
    follow_up_date: Optional[str]
    follow_up_instructions: Optional[str]
    
    discharge_summary: Optional[str]
    discharge_date: Optional[str]
    discharge_instructions: Optional[str]
    
    allergies: Optional[str]
    alerts: Optional[str]
    attachments: Optional[str]
    
    notes: Optional[str]
    doctor_notes: Optional[str]
    nurse_notes: Optional[str]
    
    status: str
    is_confidential: bool
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# List Response
class MedicalRecordListResponse(BaseModel):
    total: int
    items: list[MedicalRecordResponse]
    page: int
    page_size: int
    total_pages: int


# Vital Signs Schema
class VitalSignsSchema(BaseModel):
    temperature: Optional[str] = Field(None, max_length=10)
    blood_pressure: Optional[str] = Field(None, max_length=20)
    pulse_rate: Optional[str] = Field(None, max_length=10)
    respiratory_rate: Optional[str] = Field(None, max_length=10)
    oxygen_saturation: Optional[str] = Field(None, max_length=10)
    weight: Optional[str] = Field(None, max_length=10)
    height: Optional[str] = Field(None, max_length=10)
    bmi: Optional[str] = Field(None, max_length=10)