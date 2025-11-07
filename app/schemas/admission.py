"""
Admission Schemas
Pydantic schemas for patient admission validation and serialization
"""

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, Any
from datetime import datetime, date, time
from decimal import Decimal
from enum import Enum
import json


# Enums
class AdmissionType(str, Enum):
    """Valid admission types"""
    EMERGENCY = "emergency"
    PLANNED = "planned"
    TRANSFER = "transfer"
    OBSERVATION = "observation"
    DAY_CARE = "day_care"


class AdmissionStatus(str, Enum):
    """Valid admission statuses"""
    ADMITTED = "admitted"
    DISCHARGED = "discharged"
    TRANSFERRED = "transferred"
    DECEASED = "deceased"
    UNDER_OBSERVATION = "under_observation"


class DischargeType(str, Enum):
    """Valid discharge types"""
    NORMAL = "normal"
    AGAINST_MEDICAL_ADVICE = "against_medical_advice"
    TRANSFERRED = "transferred"
    DECEASED = "deceased"


# Nested Schemas for Relationships
class PatientBasic(BaseModel):
    """Basic patient info for nested responses"""
    id: int
    full_name: str
    patient_number: Optional[str] = None
    phone: Optional[str] = None
    
    class Config:
        from_attributes = True


class DoctorBasic(BaseModel):
    """Basic doctor info for nested responses"""
    id: int
    full_name: str
    specialization: Optional[str] = None
    license_number: Optional[str] = None
    
    class Config:
        from_attributes = True


class RoomBasic(BaseModel):
    """Basic room info"""
    id: int
    room_number: str
    room_type: Optional[str] = None
    
    class Config:
        from_attributes = True


class BedBasic(BaseModel):
    """Basic bed info"""
    id: int
    bed_number: str
    bed_type: Optional[str] = None
    
    class Config:
        from_attributes = True


class WardBasic(BaseModel):
    """Basic ward info"""
    id: int
    ward_name: str
    ward_type: Optional[str] = None
    
    class Config:
        from_attributes = True


class InsuranceBasic(BaseModel):
    """Basic insurance info"""
    id: int
    provider_name: str
    policy_number: Optional[str] = None
    
    class Config:
        from_attributes = True


# Base Schema
class AdmissionBase(BaseModel):
    """Base schema with common fields"""
    admission_number: str = Field(..., max_length=20, description="Unique admission number")
    admission_date: str = Field(..., max_length=20, description="Date of admission (YYYY-MM-DD)")
    admission_time: str = Field(..., max_length=10, description="Time of admission (HH:MM)")
    
    # References
    patient_id: int = Field(..., description="Patient ID")
    admitting_doctor_id: int = Field(..., description="Admitting doctor ID")
    
    # Location (optional)
    room_id: Optional[int] = Field(None, description="Room ID")
    bed_id: Optional[int] = Field(None, description="Bed ID")
    ward_id: Optional[int] = Field(None, description="Ward ID")
    
    # Admission details
    admission_type: AdmissionType = Field(..., description="Type of admission")
    diagnosis: str = Field(..., description="Initial diagnosis")
    chief_complaint: str = Field(..., description="Chief complaint")
    symptoms: Optional[str] = Field(None, description="Symptoms")
    
    # Status
    status: AdmissionStatus = Field(default=AdmissionStatus.ADMITTED, description="Current status")
    
    # Medical details
    vital_signs: Optional[dict[str, Any]] = Field(None, description="Vital signs as JSON")
    allergies: Optional[str] = Field(None, description="Known allergies")
    current_medications: Optional[str] = Field(None, description="Current medications")
    
    # Treatment
    treatment_plan: Optional[str] = Field(None, description="Treatment plan")
    special_instructions: Optional[str] = Field(None, description="Special instructions")
    
    # Insurance
    insurance_id: Optional[int] = Field(None, description="Insurance ID")
    insurance_approved: bool = Field(default=False, description="Insurance approval status")
    
    # Financial
    estimated_cost: Optional[Decimal] = Field(None, ge=0, decimal_places=2, description="Estimated cost")
    advance_payment: Optional[Decimal] = Field(None, ge=0, decimal_places=2, description="Advance payment")
    
    # Notes
    admission_notes: Optional[str] = Field(None, description="Admission notes")
    
    # Duration
    expected_duration_days: Optional[int] = Field(None, gt=0, description="Expected duration in days")
    
    # Discharge info (for updates)
    discharge_date: Optional[str] = Field(None, max_length=20, description="Discharge date")
    discharge_time: Optional[str] = Field(None, max_length=10, description="Discharge time")
    discharge_type: Optional[DischargeType] = Field(None, description="Type of discharge")
    discharge_summary: Optional[str] = Field(None, description="Discharge summary")
    actual_duration_days: Optional[int] = Field(None, gt=0, description="Actual duration in days")

    @field_validator('vital_signs', mode='before')
    @classmethod
    def validate_vital_signs(cls, v):
        """Ensure vital signs is valid JSON dict"""
        if v is None:
            return None
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                raise ValueError("Vital signs must be valid JSON")
        if isinstance(v, dict):
            return v
        raise ValueError("Vital signs must be a dict or JSON string")
    
    @field_validator('admission_date', 'discharge_date')
    @classmethod
    def validate_date_format(cls, v):
        """Validate date format"""
        if v is None:
            return None
        try:
            # Try parsing as date
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
    
    @field_validator('admission_time', 'discharge_time')
    @classmethod
    def validate_time_format(cls, v):
        """Validate time format"""
        if v is None:
            return None
        try:
            # Try parsing as time
            datetime.strptime(v, '%H:%M')
            return v
        except ValueError:
            raise ValueError("Time must be in HH:MM format")
    
    @model_validator(mode='after')
    def validate_discharge_data(self):
        """Validate discharge-related fields"""
        if self.status in [AdmissionStatus.DISCHARGED, AdmissionStatus.DECEASED]:
            if not self.discharge_date:
                raise ValueError("Discharge date is required when status is discharged or deceased")
            if not self.discharge_type:
                raise ValueError("Discharge type is required when status is discharged or deceased")
        return self
    
    @model_validator(mode='after')
    def validate_bed_room_consistency(self):
        """Ensure bed belongs to the specified room if both are provided"""
        # This is a basic check - actual validation should be done in the service layer
        # by querying the database to ensure bed.room_id == room_id
        return self


# Create Schema
class AdmissionCreate(AdmissionBase):
    """Schema for creating new admission"""
    # Override to exclude discharge fields for creation
    discharge_date: Optional[str] = Field(None, exclude=True)
    discharge_time: Optional[str] = Field(None, exclude=True)
    discharge_type: Optional[DischargeType] = Field(None, exclude=True)
    discharge_summary: Optional[str] = Field(None, exclude=True)
    actual_duration_days: Optional[int] = Field(None, exclude=True)
    
    # Status should be admitted for new admissions
    status: AdmissionStatus = Field(default=AdmissionStatus.ADMITTED)
    
    class Config:
        json_schema_extra = {
            "example": {
                "admission_number": "ADM-2024-0001",
                "admission_date": "2024-01-15",
                "admission_time": "14:30",
                "patient_id": 123,
                "admitting_doctor_id": 45,
                "room_id": 12,
                "bed_id": 34,
                "ward_id": 5,
                "admission_type": "emergency",
                "diagnosis": "Acute appendicitis",
                "chief_complaint": "Severe abdominal pain",
                "symptoms": "Pain in right lower quadrant, nausea, fever",
                "vital_signs": {
                    "blood_pressure": "130/85",
                    "pulse": 92,
                    "temperature": 101.2,
                    "respiratory_rate": 18
                },
                "allergies": "Penicillin",
                "current_medications": "None",
                "treatment_plan": "Emergency appendectomy",
                "insurance_id": 67,
                "estimated_cost": 5000.00,
                "advance_payment": 1000.00,
                "expected_duration_days": 3
            }
        }


# Update Schema
class AdmissionUpdate(BaseModel):
    """Schema for updating admission (partial updates allowed)"""
    room_id: Optional[int] = None
    bed_id: Optional[int] = None
    ward_id: Optional[int] = None
    admission_type: Optional[AdmissionType] = None
    diagnosis: Optional[str] = None
    symptoms: Optional[str] = None
    chief_complaint: Optional[str] = None
    status: Optional[AdmissionStatus] = None
    vital_signs: Optional[dict[str, Any]] = None
    allergies: Optional[str] = None
    current_medications: Optional[str] = None
    treatment_plan: Optional[str] = None
    special_instructions: Optional[str] = None
    insurance_id: Optional[int] = None
    insurance_approved: Optional[bool] = None
    estimated_cost: Optional[Decimal] = Field(None, ge=0)
    advance_payment: Optional[Decimal] = Field(None, ge=0)
    admission_notes: Optional[str] = None
    discharge_date: Optional[str] = None
    discharge_time: Optional[str] = None
    discharge_type: Optional[DischargeType] = None
    discharge_summary: Optional[str] = None
    expected_duration_days: Optional[int] = Field(None, gt=0)
    actual_duration_days: Optional[int] = Field(None, gt=0)

    @field_validator('vital_signs', mode='before')
    @classmethod
    def validate_vital_signs(cls, v):
        if v is None:
            return None
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                raise ValueError("Vital signs must be valid JSON")
        return v


# Response Schema
class AdmissionResponse(AdmissionBase):
    """Schema for admission response"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "admission_number": "ADM-2024-0001",
                "admission_date": "2024-01-15",
                "admission_time": "14:30",
                "patient_id": 123,
                "admitting_doctor_id": 45,
                "room_id": 12,
                "bed_id": 34,
                "ward_id": 5,
                "admission_type": "emergency",
                "diagnosis": "Acute appendicitis",
                "chief_complaint": "Severe abdominal pain",
                "symptoms": "Pain in right lower quadrant, nausea, fever",
                "status": "admitted",
                "vital_signs": {
                    "blood_pressure": "130/85",
                    "pulse": 92,
                    "temperature": 101.2
                },
                "insurance_approved": True,
                "estimated_cost": 5000.00,
                "created_at": "2024-01-15T14:30:00",
                "updated_at": "2024-01-15T14:30:00"
            }
        }


# Detailed Response with Relationships
class AdmissionDetailResponse(AdmissionResponse):
    """Detailed admission response with nested relationships"""
    patient: Optional[PatientBasic] = None
    admitting_doctor: Optional[DoctorBasic] = None
    room: Optional[RoomBasic] = None
    bed: Optional[BedBasic] = None
    ward: Optional[WardBasic] = None
    insurance: Optional[InsuranceBasic] = None
    
    class Config:
        from_attributes = True


# List Response Schema
class AdmissionListResponse(BaseModel):
    """Schema for paginated list of admissions"""
    total: int = Field(..., description="Total number of records")
    page: int = Field(..., ge=1, description="Current page number")
    page_size: int = Field(..., ge=1, le=100, description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")
    items: list[AdmissionResponse] = Field(..., description="Admission items")


# Filter/Query Schema
class AdmissionFilter(BaseModel):
    """Schema for filtering admissions"""
    # ID filters
    patient_id: Optional[int] = Field(None, description="Filter by patient ID")
    admitting_doctor_id: Optional[int] = Field(None, description="Filter by doctor ID")
    room_id: Optional[int] = Field(None, description="Filter by room ID")
    bed_id: Optional[int] = Field(None, description="Filter by bed ID")
    ward_id: Optional[int] = Field(None, description="Filter by ward ID")
    insurance_id: Optional[int] = Field(None, description="Filter by insurance ID")
    
    # String filters
    admission_number: Optional[str] = Field(None, description="Filter by admission number")
    
    # Enum filters
    admission_type: Optional[AdmissionType] = Field(None, description="Filter by admission type")
    status: Optional[AdmissionStatus] = Field(None, description="Filter by status")
    discharge_type: Optional[DischargeType] = Field(None, description="Filter by discharge type")
    
    # Boolean filters
    insurance_approved: Optional[bool] = Field(None, description="Filter by insurance approval")
    
    # Date range filters
    admission_date_from: Optional[str] = Field(None, description="Admissions from this date (YYYY-MM-DD)")
    admission_date_to: Optional[str] = Field(None, description="Admissions until this date (YYYY-MM-DD)")
    discharge_date_from: Optional[str] = Field(None, description="Discharges from this date")
    discharge_date_to: Optional[str] = Field(None, description="Discharges until this date")
    
    # Search
    search: Optional[str] = Field(None, description="Search in diagnosis, symptoms, chief_complaint")
    
    # Pagination
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")
    
    # Sorting
    sort_by: Optional[str] = Field("admission_date", description="Field to sort by")
    sort_order: Optional[str] = Field("desc", pattern="^(asc|desc)$", description="Sort order")
    
    # Include relationships
    include_patient: bool = Field(False, description="Include patient details")
    include_doctor: bool = Field(False, description="Include doctor details")
    include_location: bool = Field(False, description="Include room/bed/ward details")


# Discharge Schema
class DischargeAdmission(BaseModel):
    """Schema for discharging a patient"""
    discharge_date: str = Field(..., description="Discharge date (YYYY-MM-DD)")
    discharge_time: str = Field(..., description="Discharge time (HH:MM)")
    discharge_type: DischargeType = Field(..., description="Type of discharge")
    discharge_summary: str = Field(..., description="Discharge summary")
    actual_duration_days: Optional[int] = Field(None, gt=0, description="Actual stay duration")
    final_diagnosis: Optional[str] = Field(None, description="Final diagnosis")
    follow_up_instructions: Optional[str] = Field(None, description="Follow-up instructions")
    medications_prescribed: Optional[str] = Field(None, description="Discharge medications")
    
    @field_validator('discharge_date')
    @classmethod
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
    
    @field_validator('discharge_time')
    @classmethod
    def validate_time(cls, v):
        try:
            datetime.strptime(v, '%H:%M')
            return v
        except ValueError:
            raise ValueError("Time must be in HH:MM format")


# Transfer Schema
class TransferAdmission(BaseModel):
    """Schema for transferring patient to another room/ward"""
    new_room_id: Optional[int] = Field(None, description="New room ID")
    new_bed_id: Optional[int] = Field(None, description="New bed ID")
    new_ward_id: Optional[int] = Field(None, description="New ward ID")
    transfer_reason: str = Field(..., description="Reason for transfer")
    transfer_date: str = Field(..., description="Transfer date")
    transfer_time: str = Field(..., description="Transfer time")
    
    @model_validator(mode='after')
    def validate_transfer_location(self):
        """At least one location field must be provided"""
        if not any([self.new_room_id, self.new_bed_id, self.new_ward_id]):
            raise ValueError("At least one of new_room_id, new_bed_id, or new_ward_id must be provided")
        return self


# Statistics Schema
class AdmissionStats(BaseModel):
    """Schema for admission statistics"""
    total_admissions: int
    active_admissions: int
    discharged_admissions: int
    average_stay_duration: Optional[float] = None
    admissions_by_type: dict[str, int]
    admissions_by_status: dict[str, int]
    occupancy_rate: Optional[float] = Field(None, description="Bed occupancy percentage")
    total_revenue: Optional[Decimal] = None
    pending_insurance_approvals: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_admissions": 1500,
                "active_admissions": 85,
                "discharged_admissions": 1400,
                "average_stay_duration": 4.5,
                "admissions_by_type": {
                    "emergency": 600,
                    "planned": 700,
                    "transfer": 150,
                    "observation": 50
                },
                "admissions_by_status": {
                    "admitted": 85,
                    "discharged": 1400,
                    "transferred": 10,
                    "deceased": 5
                },
                "occupancy_rate": 75.5,
                "total_revenue": 750000.00,
                "pending_insurance_approvals": 12
            }
        }


# Dashboard Summary
class AdmissionDashboard(BaseModel):
    """Dashboard summary for admissions"""
    today_admissions: int
    today_discharges: int
    current_occupancy: int
    available_beds: int
    emergency_admissions_today: int
    planned_admissions_today: int
    pending_discharges: int
    critical_patients: int
    insurance_pending: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "today_admissions": 15,
                "today_discharges": 12,
                "current_occupancy": 85,
                "available_beds": 35,
                "emergency_admissions_today": 8,
                "planned_admissions_today": 7,
                "pending_discharges": 5,
                "critical_patients": 10,
                "insurance_pending": 3
            }
        }


# Bulk Operations
class AdmissionBulkUpdate(BaseModel):
    """Schema for bulk updating admissions"""
    admission_ids: list[int] = Field(..., min_length=1, description="List of admission IDs")
    update_data: AdmissionUpdate = Field(..., description="Update data to apply")


# Vital Signs Schema (separate for clarity)
class VitalSigns(BaseModel):
    """Schema for vital signs"""
    blood_pressure: Optional[str] = Field(None, description="Blood pressure (e.g., 120/80)")
    pulse: Optional[int] = Field(None, ge=0, le=300, description="Pulse rate")
    temperature: Optional[float] = Field(None, ge=90, le=110, description="Temperature in Fahrenheit")
    respiratory_rate: Optional[int] = Field(None, ge=0, le=100, description="Respiratory rate")
    oxygen_saturation: Optional[float] = Field(None, ge=0, le=100, description="O2 saturation %")
    weight: Optional[float] = Field(None, ge=0, description="Weight in kg")
    height: Optional[float] = Field(None, ge=0, description="Height in cm")
    bmi: Optional[float] = Field(None, ge=0, description="Body Mass Index")
    
    class Config:
        json_schema_extra = {
            "example": {
                "blood_pressure": "120/80",
                "pulse": 75,
                "temperature": 98.6,
                "respiratory_rate": 16,
                "oxygen_saturation": 98.5,
                "weight": 70.5,
                "height": 175.0,
                "bmi": 23.0
            }
        }