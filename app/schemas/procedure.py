"""
Procedure Schemas
"""

from pydantic import BaseModel, Field, validator, condecimal
from typing import Optional
from datetime import datetime
from decimal import Decimal


# Base Schema
class ProcedureBase(BaseModel):
    procedure_number: str = Field(..., max_length=20, description="Unique procedure number")
    patient_id: int = Field(..., gt=0)
    doctor_id: int = Field(..., gt=0)
    procedure_name: str = Field(..., max_length=200)
    category: str = Field(..., max_length=100)
    
    @validator('category')
    def validate_category(cls, v):
        valid = ['surgical', 'diagnostic', 'therapeutic', 'preventive', 'cosmetic']
        if v.lower() not in valid:
            raise ValueError(f"Category must be one of: {', '.join(valid)}")
        return v.lower()


# Create Schema
class ProcedureCreate(ProcedureBase):
    procedure_code: Optional[str] = Field(None, max_length=50)
    
    procedure_type: str = Field(default='minor', max_length=50)
    
    description: Optional[str] = None
    indications: Optional[str] = None
    
    scheduled_date: str = Field(..., max_length=20)
    scheduled_time: str = Field(..., max_length=10)
    procedure_date: Optional[str] = Field(None, max_length=20)
    procedure_time: Optional[str] = Field(None, max_length=10)
    
    estimated_duration: Optional[int] = Field(None, gt=0, description="Duration in minutes")
    actual_duration: Optional[int] = Field(None, gt=0)
    
    room_number: Optional[str] = Field(None, max_length=50)
    operation_theater: Optional[str] = Field(None, max_length=100)
    
    assisting_doctors: Optional[str] = Field(None, description="JSON array")
    nurses_assigned: Optional[str] = Field(None, description="JSON array")
    anesthetist: Optional[str] = Field(None, max_length=200)
    
    anesthesia_type: Optional[str] = Field(None, max_length=50)
    anesthesia_notes: Optional[str] = None
    
    pre_procedure_instructions: Optional[str] = None
    pre_procedure_tests: Optional[str] = Field(None, description="JSON array")
    consent_obtained: bool = Field(default=False)
    consent_date: Optional[str] = Field(None, max_length=20)
    
    findings: Optional[str] = None
    technique_used: Optional[str] = None
    complications: Optional[str] = None
    
    specimens_collected: Optional[str] = Field(None, description="JSON array")
    pathology_required: bool = Field(default=False)
    
    post_procedure_instructions: Optional[str] = None
    recovery_notes: Optional[str] = None
    discharge_time: Optional[str] = Field(None, max_length=50)
    
    follow_up_required: bool = Field(default=False)
    follow_up_date: Optional[str] = Field(None, max_length=20)
    follow_up_instructions: Optional[str] = None
    
    status: str = Field(default='scheduled', max_length=20)
    outcome: Optional[str] = Field(None, max_length=50)
    priority: str = Field(default='routine', max_length=20)
    
    estimated_cost: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    actual_cost: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    
    procedure_report_url: Optional[str] = Field(None, max_length=500)
    images_urls: Optional[str] = Field(None, description="JSON array")
    consent_form_url: Optional[str] = Field(None, max_length=500)
    
    doctor_notes: Optional[str] = None
    nurse_notes: Optional[str] = None
    notes: Optional[str] = None
    
    @validator('procedure_type')
    def validate_procedure_type(cls, v):
        valid = ['minor', 'major', 'emergency', 'elective']
        if v.lower() not in valid:
            raise ValueError(f"Procedure type must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validator('status')
    def validate_status(cls, v):
        valid = ['scheduled', 'in_progress', 'completed', 'cancelled', 'postponed']
        if v.lower() not in valid:
            raise ValueError(f"Status must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validator('priority')
    def validate_priority(cls, v):
        valid = ['routine', 'urgent', 'emergency']
        if v.lower() not in valid:
            raise ValueError(f"Priority must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validator('anesthesia_type')
    def validate_anesthesia_type(cls, v):
        if v:
            valid = ['local', 'general', 'regional', 'sedation', 'none']
            if v.lower() not in valid:
                raise ValueError(f"Anesthesia type must be one of: {', '.join(valid)}")
            return v.lower()
        return v


# Update Schema
class ProcedureUpdate(BaseModel):
    procedure_name: Optional[str] = Field(None, max_length=200)
    procedure_code: Optional[str] = Field(None, max_length=50)
    category: Optional[str] = Field(None, max_length=100)
    procedure_type: Optional[str] = Field(None, max_length=50)
    
    description: Optional[str] = None
    indications: Optional[str] = None
    
    scheduled_date: Optional[str] = Field(None, max_length=20)
    scheduled_time: Optional[str] = Field(None, max_length=10)
    procedure_date: Optional[str] = Field(None, max_length=20)
    procedure_time: Optional[str] = Field(None, max_length=10)
    
    estimated_duration: Optional[int] = Field(None, gt=0)
    actual_duration: Optional[int] = Field(None, gt=0)
    
    room_number: Optional[str] = Field(None, max_length=50)
    operation_theater: Optional[str] = Field(None, max_length=100)
    
    assisting_doctors: Optional[str] = None
    nurses_assigned: Optional[str] = None
    anesthetist: Optional[str] = Field(None, max_length=200)
    
    anesthesia_type: Optional[str] = Field(None, max_length=50)
    anesthesia_notes: Optional[str] = None
    
    pre_procedure_instructions: Optional[str] = None
    pre_procedure_tests: Optional[str] = None
    consent_obtained: Optional[bool] = None
    consent_date: Optional[str] = Field(None, max_length=20)
    
    findings: Optional[str] = None
    technique_used: Optional[str] = None
    complications: Optional[str] = None
    
    specimens_collected: Optional[str] = None
    pathology_required: Optional[bool] = None
    
    post_procedure_instructions: Optional[str] = None
    recovery_notes: Optional[str] = None
    discharge_time: Optional[str] = Field(None, max_length=50)
    
    follow_up_required: Optional[bool] = None
    follow_up_date: Optional[str] = Field(None, max_length=20)
    follow_up_instructions: Optional[str] = None
    
    status: Optional[str] = Field(None, max_length=20)
    outcome: Optional[str] = Field(None, max_length=50)
    priority: Optional[str] = Field(None, max_length=20)
    
    estimated_cost: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    actual_cost: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    
    procedure_report_url: Optional[str] = Field(None, max_length=500)
    images_urls: Optional[str] = None
    consent_form_url: Optional[str] = Field(None, max_length=500)
    
    doctor_notes: Optional[str] = None
    nurse_notes: Optional[str] = None
    notes: Optional[str] = None


# Response Schema
class ProcedureResponse(ProcedureBase):
    id: int
    procedure_code: Optional[str]
    
    procedure_type: str
    
    description: Optional[str]
    indications: Optional[str]
    
    scheduled_date: str
    scheduled_time: str
    procedure_date: Optional[str]
    procedure_time: Optional[str]
    
    estimated_duration: Optional[int]
    actual_duration: Optional[int]
    
    room_number: Optional[str]
    operation_theater: Optional[str]
    
    assisting_doctors: Optional[str]
    nurses_assigned: Optional[str]
    anesthetist: Optional[str]
    
    anesthesia_type: Optional[str]
    anesthesia_notes: Optional[str]
    
    pre_procedure_instructions: Optional[str]
    pre_procedure_tests: Optional[str]
    consent_obtained: bool
    consent_date: Optional[str]
    
    findings: Optional[str]
    technique_used: Optional[str]
    complications: Optional[str]
    
    specimens_collected: Optional[str]
    pathology_required: bool
    
    post_procedure_instructions: Optional[str]
    recovery_notes: Optional[str]
    discharge_time: Optional[str]
    
    follow_up_required: bool
    follow_up_date: Optional[str]
    follow_up_instructions: Optional[str]
    
    status: str
    outcome: Optional[str]
    priority: str
    
    estimated_cost: Optional[Decimal]
    actual_cost: Optional[Decimal]
    
    procedure_report_url: Optional[str]
    images_urls: Optional[str]
    consent_form_url: Optional[str]
    
    doctor_notes: Optional[str]
    nurse_notes: Optional[str]
    notes: Optional[str]
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v)
        }


# List Response
class ProcedureListResponse(BaseModel):
    total: int
    items: list[ProcedureResponse]
    page: int
    page_size: int
    total_pages: int


# Complete Procedure Schema
class ProcedureCompleteSchema(BaseModel):
    procedure_date: str = Field(..., max_length=20)
    procedure_time: str = Field(..., max_length=10)
    actual_duration: int = Field(..., gt=0, description="Duration in minutes")
    findings: str = Field(..., description="Procedure findings")
    technique_used: str = Field(..., description="Technique used")
    outcome: str = Field(..., max_length=50, description="successful, unsuccessful, partial_success")
    actual_cost: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    doctor_notes: Optional[str] = None