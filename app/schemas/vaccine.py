"""
Vaccine Schemas
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


# Base Schema
class VaccineBase(BaseModel):
    vaccination_number: str = Field(..., max_length=20, description="Unique vaccination number")
    patient_id: int = Field(..., gt=0)
    vaccine_name: str = Field(..., max_length=200)
    vaccine_type: str = Field(..., max_length=100)
    
    @validator('vaccine_type')
    def validate_vaccine_type(cls, v):
        valid = [
            'covid_19', 'influenza', 'hepatitis_a', 'hepatitis_b', 'mmr',
            'polio', 'tetanus', 'dpt', 'bcg', 'hpv', 'meningitis',
            'pneumonia', 'rabies', 'typhoid', 'yellow_fever', 'cholera'
        ]
        if v.lower() not in valid:
            raise ValueError(f"Vaccine type must be one of: {', '.join(valid)}")
        return v.lower()


# Create Schema
class VaccineCreate(VaccineBase):
    doctor_id: Optional[int] = None
    
    vaccine_code: Optional[str] = Field(None, max_length=50)
    
    # Manufacturer
    manufacturer: str = Field(..., max_length=200)
    batch_number: str = Field(..., max_length=100)
    lot_number: Optional[str] = Field(None, max_length=100)
    expiry_date: str = Field(..., max_length=20)
    
    # Dose Information
    dose_number: int = Field(default=1, ge=1)
    total_doses_required: Optional[int] = Field(None, ge=1)
    dosage: Optional[str] = Field(None, max_length=50)
    
    # Administration
    administered_date: str = Field(..., max_length=20)
    administered_time: str = Field(..., max_length=10)
    administered_by: str = Field(..., max_length=200)
    nurse_id: Optional[int] = None
    
    # Site and Route
    site_of_injection: str = Field(..., max_length=100)
    route_of_administration: str = Field(default='intramuscular', max_length=50)
    
    # Next Dose
    next_dose_due: bool = Field(default=False)
    next_dose_date: Optional[str] = Field(None, max_length=20)
    next_dose_number: Optional[int] = Field(None, ge=1)
    
    # Pre-Vaccination
    temperature: Optional[str] = Field(None, max_length=10)
    blood_pressure: Optional[str] = Field(None, max_length=20)
    
    screening_done: bool = Field(default=True)
    contraindications_checked: bool = Field(default=True)
    consent_obtained: bool = Field(default=True)
    consent_form_url: Optional[str] = Field(None, max_length=500)
    
    # Adverse Reactions
    has_adverse_reaction: bool = Field(default=False)
    adverse_reactions: Optional[str] = None
    reaction_severity: Optional[str] = Field(None, max_length=20)
    reaction_reported: bool = Field(default=False)
    reaction_report_number: Optional[str] = Field(None, max_length=50)
    
    # Post-Vaccination
    observation_period_minutes: int = Field(default=15, ge=0)
    observation_notes: Optional[str] = None
    
    # Certificate
    certificate_number: Optional[str] = Field(None, max_length=100)
    certificate_url: Optional[str] = Field(None, max_length=500)
    
    # Storage Verification
    storage_temperature_verified: bool = Field(default=True)
    cold_chain_maintained: bool = Field(default=True)
    
    # Campaign
    vaccination_program: Optional[str] = Field(None, max_length=200)
    is_part_of_campaign: bool = Field(default=False)
    campaign_name: Optional[str] = Field(None, max_length=200)
    
    # Cost
    is_free: bool = Field(default=False)
    cost: Optional[str] = Field(None, max_length=50)
    
    # Notes
    notes: Optional[str] = None
    doctor_notes: Optional[str] = None
    
    # Status
    status: str = Field(default='completed', max_length=20)
    
    @validator('route_of_administration')
    def validate_route(cls, v):
        valid = ['intramuscular', 'subcutaneous', 'oral', 'intranasal', 'intradermal']
        if v.lower() not in valid:
            raise ValueError(f"Route must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validator('status')
    def validate_status(cls, v):
        valid = ['scheduled', 'completed', 'cancelled', 'postponed', 'missed']
        if v.lower() not in valid:
            raise ValueError(f"Status must be one of: {', '.join(valid)}")
        return v.lower()


# Update Schema
class VaccineUpdate(BaseModel):
    has_adverse_reaction: Optional[bool] = None
    adverse_reactions: Optional[str] = None
    reaction_severity: Optional[str] = Field(None, max_length=20)
    reaction_reported: Optional[bool] = None
    reaction_report_number: Optional[str] = Field(None, max_length=50)
    
    observation_notes: Optional[str] = None
    
    certificate_number: Optional[str] = Field(None, max_length=100)
    certificate_url: Optional[str] = Field(None, max_length=500)
    
    next_dose_due: Optional[bool] = None
    next_dose_date: Optional[str] = Field(None, max_length=20)
    next_dose_number: Optional[int] = Field(None, ge=1)
    
    notes: Optional[str] = None
    doctor_notes: Optional[str] = None
    
    status: Optional[str] = Field(None, max_length=20)


# Response Schema
class VaccineResponse(VaccineBase):
    id: int
    doctor_id: Optional[int]
    
    vaccine_code: Optional[str]
    
    manufacturer: str
    batch_number: str
    lot_number: Optional[str]
    expiry_date: str
    
    dose_number: int
    total_doses_required: Optional[int]
    dosage: Optional[str]
    
    administered_date: str
    administered_time: str
    administered_by: str
    nurse_id: Optional[int]
    
    site_of_injection: str
    route_of_administration: str
    
    next_dose_due: bool
    next_dose_date: Optional[str]
    next_dose_number: Optional[int]
    
    temperature: Optional[str]
    blood_pressure: Optional[str]
    
    screening_done: bool
    contraindications_checked: bool
    consent_obtained: bool
    consent_form_url: Optional[str]
    
    has_adverse_reaction: bool
    adverse_reactions: Optional[str]
    reaction_severity: Optional[str]
    reaction_reported: bool
    reaction_report_number: Optional[str]
    
    observation_period_minutes: int
    observation_notes: Optional[str]
    
    certificate_number: Optional[str]
    certificate_url: Optional[str]
    
    storage_temperature_verified: bool
    cold_chain_maintained: bool
    
    vaccination_program: Optional[str]
    is_part_of_campaign: bool
    campaign_name: Optional[str]
    
    is_free: bool
    cost: Optional[str]
    
    notes: Optional[str]
    doctor_notes: Optional[str]
    
    status: str
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# List Response
class VaccineListResponse(BaseModel):
    total: int
    items: list[VaccineResponse]
    page: int
    page_size: int
    total_pages: int


# Vaccination Schedule Schema
class VaccinationScheduleSchema(BaseModel):
    patient_id: int = Field(..., gt=0)
    vaccine_type: str = Field(..., max_length=100)
    
    scheduled_date: str = Field(..., max_length=20)
    scheduled_time: str = Field(..., max_length=10)
    
    dose_number: int = Field(..., ge=1)
    
    doctor_id: Optional[int] = None
    notes: Optional[str] = None


# Immunization Record Schema
class ImmunizationRecordSchema(BaseModel):
    patient_id: int
    patient_name: str
    date_of_birth: str
    
    vaccinations: list[VaccineResponse]
    
    total_vaccines_received: int
    pending_vaccines: list[dict]  # {vaccine_name, due_date}
    overdue_vaccines: list[dict]
    
    last_vaccination_date: Optional[str]
    next_vaccination_due: Optional[str]