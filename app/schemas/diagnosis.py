"""
Diagnosis Schemas
Pydantic schemas for patient diagnosis management and medical coding
"""

from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from typing import Optional, Any, List, Dict, Union
from datetime import datetime, date, timedelta
from decimal import Decimal
from enum import Enum
import json
import re


# Enums
class DiagnosisType(str, Enum):
    """Valid diagnosis types"""
    PRIMARY = "primary"
    SECONDARY = "secondary"
    DIFFERENTIAL = "differential"
    PROVISIONAL = "provisional"
    CONFIRMED = "confirmed"
    RULE_OUT = "rule_out"
    WORKING = "working"
    ADMISSION = "admission"
    DISCHARGE = "discharge"


class DiagnosisSeverity(str, Enum):
    """Severity levels"""
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    CRITICAL = "critical"


class DiagnosisStatus(str, Enum):
    """Diagnosis status"""
    ACTIVE = "active"
    RESOLVED = "resolved"
    CHRONIC = "chronic"
    UNDER_OBSERVATION = "under_observation"
    RULED_OUT = "ruled_out"
    INACTIVE = "inactive"
    RECURRENT = "recurrent"


class ICDVersion(str, Enum):
    """ICD coding versions"""
    ICD_9 = "ICD-9"
    ICD_10 = "ICD-10"
    ICD_11 = "ICD-11"


class Prognosis(str, Enum):
    """Prognosis options"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    GRAVE = "grave"
    UNCERTAIN = "uncertain"


class Laterality(str, Enum):
    """Anatomical laterality"""
    LEFT = "left"
    RIGHT = "right"
    BILATERAL = "bilateral"
    UNILATERAL = "unilateral"
    MIDLINE = "midline"


class ConfirmationMethod(str, Enum):
    """Diagnosis confirmation methods"""
    CLINICAL = "clinical"
    LABORATORY = "laboratory"
    IMAGING = "imaging"
    BIOPSY = "biopsy"
    GENETIC_TEST = "genetic_test"
    PATHOLOGY = "pathology"
    ENDOSCOPY = "endoscopy"


class Priority(str, Enum):
    """Diagnosis priority"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


# Helper Schemas
class ICDCode(BaseModel):
    """ICD code information"""
    code: str = Field(..., max_length=20, description="ICD code")
    version: ICDVersion = Field(..., description="ICD version")
    description: str = Field(..., description="Code description")
    category: Optional[str] = Field(None, description="Disease category")
    billable: bool = Field(default=True, description="Whether code is billable")
    
    @field_validator('code')
    @classmethod
    def validate_icd_code(cls, v):
        """Validate ICD code format"""
        # Basic validation - ICD-10 format: A00.0
        if not re.match(r'^[A-Z][0-9]{2}\.?[0-9A-Z]*$', v):
            raise ValueError("Invalid ICD code format")
        return v.upper()
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": "J18.9",
                "version": "ICD-10",
                "description": "Pneumonia, unspecified organism",
                "category": "Respiratory diseases",
                "billable": True
            }
        }


class ClinicalFinding(BaseModel):
    """Clinical examination finding"""
    finding: str = Field(..., description="Clinical finding")
    body_site: Optional[str] = Field(None, description="Anatomical location")
    severity: Optional[DiagnosisSeverity] = None
    notes: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "finding": "Crackles in lower lung fields",
                "body_site": "Lungs - bilateral lower lobes",
                "severity": "moderate",
                "notes": "More prominent on right side"
            }
        }


class DifferentialDiagnosis(BaseModel):
    """Alternative diagnosis consideration"""
    diagnosis_name: str = Field(..., description="Alternative diagnosis name")
    icd_code: Optional[str] = Field(None, description="ICD code")
    probability: Optional[str] = Field(None, pattern="^(low|moderate|high)$", description="Likelihood")
    reason: Optional[str] = Field(None, description="Reason for consideration")
    ruled_out: bool = Field(default=False, description="Whether ruled out")
    ruled_out_reason: Optional[str] = Field(None, description="Why ruled out")
    
    class Config:
        json_schema_extra = {
            "example": {
                "diagnosis_name": "Tuberculosis",
                "icd_code": "A15.0",
                "probability": "low",
                "reason": "Chronic cough with weight loss",
                "ruled_out": True,
                "ruled_out_reason": "Negative TB test and chest X-ray"
            }
        }


class Medication(BaseModel):
    """Prescribed medication"""
    medication_name: str = Field(..., description="Medication name")
    dosage: str = Field(..., description="Dosage")
    frequency: str = Field(..., description="Frequency")
    duration: Optional[str] = Field(None, description="Duration")
    route: Optional[str] = Field(None, description="Route of administration")
    instructions: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "medication_name": "Amoxicillin",
                "dosage": "500mg",
                "frequency": "Three times daily",
                "duration": "7 days",
                "route": "Oral",
                "instructions": "Take with food"
            }
        }


class Procedure(BaseModel):
    """Medical procedure"""
    procedure_name: str = Field(..., description="Procedure name")
    procedure_code: Optional[str] = Field(None, description="CPT/procedure code")
    scheduled_date: Optional[str] = Field(None, description="Scheduled date")
    status: Optional[str] = Field(None, description="Status")
    notes: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "procedure_name": "Chest X-ray",
                "procedure_code": "71046",
                "scheduled_date": "2024-01-16",
                "status": "Completed",
                "notes": "Shows bilateral infiltrates"
            }
        }


class RiskFactor(BaseModel):
    """Risk factor information"""
    factor: str = Field(..., description="Risk factor")
    type: Optional[str] = Field(None, description="Type (genetic, environmental, behavioral)")
    significance: Optional[str] = Field(None, pattern="^(low|moderate|high)$")
    notes: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "factor": "Smoking - 20 pack years",
                "type": "behavioral",
                "significance": "high",
                "notes": "Patient attempting to quit"
            }
        }


class Comorbidity(BaseModel):
    """Comorbid condition"""
    condition_name: str = Field(..., description="Condition name")
    icd_code: Optional[str] = Field(None, description="ICD code")
    status: Optional[str] = Field(None, description="Status")
    impact: Optional[str] = Field(None, description="Impact on current diagnosis")
    
    class Config:
        json_schema_extra = {
            "example": {
                "condition_name": "Type 2 Diabetes Mellitus",
                "icd_code": "E11.9",
                "status": "active",
                "impact": "May delay healing"
            }
        }


# Nested Schemas for Relationships
class PatientBasic(BaseModel):
    """Basic patient info"""
    id: int
    full_name: str
    patient_number: Optional[str] = None
    date_of_birth: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    
    class Config:
        from_attributes = True


class DoctorBasic(BaseModel):
    """Basic doctor info"""
    id: int
    full_name: str
    specialization: Optional[str] = None
    license_number: Optional[str] = None
    
    class Config:
        from_attributes = True


# Base Schema
class DiagnosisBase(BaseModel):
    """Base schema for diagnosis"""
    # Basic Info
    diagnosis_code: str = Field(..., max_length=20, description="Diagnosis code/identifier")
    diagnosis_name: str = Field(..., max_length=500, description="Diagnosis name")
    description: str = Field(..., min_length=5, description="Detailed description")
    
    # References
    patient_id: int = Field(..., description="Patient ID")
    doctor_id: int = Field(..., description="Diagnosing doctor ID")
    admission_id: Optional[int] = Field(None, description="Related admission ID")
    appointment_id: Optional[int] = Field(None, description="Related appointment ID")
    
    # Medical Coding
    icd_version: ICDVersion = Field(default=ICDVersion.ICD_10, description="ICD version")
    icd_code: str = Field(..., max_length=20, description="ICD diagnosis code")
    snomed_code: Optional[str] = Field(None, max_length=50, description="SNOMED CT code")
    dms_code: Optional[str] = Field(None, max_length=50, description="Disease management code")
    
    # Classification
    diagnosis_type: DiagnosisType = Field(..., description="Type of diagnosis")
    category: Optional[str] = Field(None, max_length=100, description="Disease category")
    severity: DiagnosisSeverity = Field(default=DiagnosisSeverity.MODERATE, description="Severity level")
    status: DiagnosisStatus = Field(default=DiagnosisStatus.ACTIVE, description="Current status")
    
    # Dates
    diagnosis_date: str = Field(..., description="Diagnosis date (YYYY-MM-DD)")
    diagnosis_time: Optional[str] = Field(None, pattern="^([01][0-9]|2[0-3]):[0-5][0-9]$", description="Time (HH:MM)")
    onset_date: Optional[str] = Field(None, description="Symptom onset date")
    resolution_date: Optional[str] = Field(None, description="Resolution date")
    
    # Clinical Details
    symptoms: Optional[str] = Field(None, description="Presenting symptoms")
    clinical_findings: Optional[str] = Field(None, description="Clinical examination findings")
    differential_diagnoses: Optional[List[str]] = Field(None, description="Alternative diagnoses")
    
    # Anatomical Location
    body_site: Optional[str] = Field(None, max_length=200, description="Anatomical location")
    laterality: Optional[Laterality] = Field(None, description="Laterality")
    
    # Staging
    stage: Optional[str] = Field(None, max_length=50, description="Disease stage")
    grade: Optional[str] = Field(None, max_length=50, description="Grade/severity classification")
    
    # Confirmation
    is_confirmed: bool = Field(default=False, description="Whether confirmed")
    confirmed_by: Optional[str] = Field(None, max_length=200, description="Confirming physician")
    confirmed_date: Optional[str] = Field(None, description="Confirmation date")
    confirmation_method: Optional[ConfirmationMethod] = Field(None, description="How confirmed")
    
    # Supporting Evidence
    lab_results: Optional[List[int]] = Field(None, description="Lab test IDs")
    imaging_results: Optional[List[int]] = Field(None, description="Imaging study IDs")
    biopsy_results: Optional[str] = Field(None, description="Biopsy results")
    
    # Treatment
    treatment_plan: Optional[str] = Field(None, description="Treatment plan")
    medications: Optional[List[str]] = Field(None, description="Prescribed medications")
    procedures: Optional[List[str]] = Field(None, description="Planned procedures")
    
    # Prognosis
    prognosis: Optional[Prognosis] = Field(None, description="Expected outcome")
    expected_outcome: Optional[str] = Field(None, description="Expected outcome description")
    
    # Follow-up
    requires_followup: bool = Field(default=False, description="Requires follow-up")
    followup_date: Optional[str] = Field(None, description="Follow-up date")
    followup_frequency: Optional[str] = Field(None, description="Follow-up frequency")
    
    # Complications & Comorbidities
    complications: Optional[str] = Field(None, description="Any complications")
    comorbidities: Optional[List[str]] = Field(None, description="Related conditions")
    risk_factors: Optional[List[str]] = Field(None, description="Risk factors")
    
    # Chronic Management
    is_chronic: bool = Field(default=False, description="Is chronic condition")
    management_plan: Optional[str] = Field(None, description="Chronic disease management plan")
    
    # Notification
    is_notifiable: bool = Field(default=False, description="Reportable disease")
    notified_to: Optional[str] = Field(None, description="Reported to authority")
    notification_date: Optional[str] = Field(None, description="Notification date")
    
    # Priority
    priority: Priority = Field(default=Priority.NORMAL, description="Priority level")
    
    # Cost
    diagnosis_cost: Optional[Decimal] = Field(None, ge=0, decimal_places=2, description="Associated cost")
    
    # Notes
    notes: Optional[str] = Field(None, description="Additional notes")
    internal_notes: Optional[str] = Field(None, description="Internal/staff notes")
    
    # Verification
    verified_by: Optional[str] = Field(None, description="Verified by")
    verified_date: Optional[str] = Field(None, description="Verification date")

    @field_validator('icd_code')
    @classmethod
    def validate_icd_code(cls, v):
        """Validate ICD code format"""
        if not re.match(r'^[A-Z][0-9]{2}\.?[0-9A-Z]*$', v):
            raise ValueError("Invalid ICD code format")
        return v.upper()
    
    @field_validator('diagnosis_date', 'onset_date', 'resolution_date', 
                     'confirmed_date', 'followup_date', 'notification_date', 'verified_date')
    @classmethod
    def validate_date_format(cls, v):
        """Validate date format"""
        if v is None:
            return None
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
    
    @field_validator('differential_diagnoses', 'lab_results', 'imaging_results', 
                     'medications', 'procedures', 'comorbidities', 'risk_factors', mode='before')
    @classmethod
    def parse_json_lists(cls, v):
        """Parse JSON lists"""
        if v is None:
            return None
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                raise ValueError("Must be valid JSON array")
        return v
    
    @model_validator(mode='after')
    def validate_confirmation(self):
        """Validate confirmation fields"""
        if self.is_confirmed:
            if not self.confirmed_date:
                raise ValueError("Confirmation date required when diagnosis is confirmed")
        return self
    
    @model_validator(mode='after')
    def validate_followup(self):
        """Validate follow-up fields"""
        if self.requires_followup and not self.followup_date:
            raise ValueError("Follow-up date required when follow-up is needed")
        return self
    
    @model_validator(mode='after')
    def validate_dates_chronology(self):
        """Validate chronological order"""
        dates = []
        
        if self.onset_date:
            dates.append(('onset', datetime.strptime(self.onset_date, '%Y-%m-%d')))
        if self.diagnosis_date:
            dates.append(('diagnosis', datetime.strptime(self.diagnosis_date, '%Y-%m-%d')))
        if self.confirmed_date:
            dates.append(('confirmed', datetime.strptime(self.confirmed_date, '%Y-%m-%d')))
        if self.resolution_date:
            dates.append(('resolution', datetime.strptime(self.resolution_date, '%Y-%m-%d')))
        
        # Onset should be before or same as diagnosis
        if self.onset_date and self.diagnosis_date:
            onset = datetime.strptime(self.onset_date, '%Y-%m-%d')
            diagnosis = datetime.strptime(self.diagnosis_date, '%Y-%m-%d')
            if onset > diagnosis:
                raise ValueError("Onset date cannot be after diagnosis date")
        
        return self


# Create Schema
class DiagnosisCreate(BaseModel):
    """Schema for creating new diagnosis"""
    # Basic required fields
    diagnosis_name: str = Field(..., max_length=500)
    description: str = Field(..., min_length=5)
    patient_id: int
    doctor_id: int
    
    # Medical coding
    icd_code: str = Field(..., max_length=20, description="ICD code (required)")
    icd_version: ICDVersion = Field(default=ICDVersion.ICD_10)
    snomed_code: Optional[str] = None
    
    # Classification
    diagnosis_type: DiagnosisType
    category: Optional[str] = None
    severity: DiagnosisSeverity = Field(default=DiagnosisSeverity.MODERATE)
    
    # Dates
    diagnosis_date: Optional[str] = Field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d'))
    diagnosis_time: Optional[str] = Field(default_factory=lambda: datetime.now().strftime('%H:%M'))
    onset_date: Optional[str] = None
    
    # Clinical
    symptoms: Optional[str] = None
    clinical_findings: Optional[List[ClinicalFinding]] = None
    differential_diagnoses: Optional[List[DifferentialDiagnosis]] = None
    
    # Location
    body_site: Optional[str] = None
    laterality: Optional[Laterality] = None
    
    # Optional associations
    admission_id: Optional[int] = None
    appointment_id: Optional[int] = None
    
    # Treatment
    treatment_plan: Optional[str] = None
    medications: Optional[List[Medication]] = None
    procedures: Optional[List[Procedure]] = None
    
    # Risk factors and comorbidities
    risk_factors: Optional[List[RiskFactor]] = None
    comorbidities: Optional[List[Comorbidity]] = None
    
    # Management
    is_chronic: bool = Field(default=False)
    requires_followup: bool = Field(default=False)
    followup_date: Optional[str] = None
    
    # Notes
    notes: Optional[str] = None
    
    # Auto-generate diagnosis code
    diagnosis_code: Optional[str] = Field(None, description="Auto-generated if not provided")
    
    class Config:
        json_schema_extra = {
            "example": {
                "diagnosis_name": "Community-acquired pneumonia",
                "description": "Pneumonia acquired outside hospital setting with typical symptoms",
                "patient_id": 123,
                "doctor_id": 45,
                "icd_code": "J18.9",
                "icd_version": "ICD-10",
                "diagnosis_type": "primary",
                "category": "Respiratory infections",
                "severity": "moderate",
                "diagnosis_date": "2024-01-15",
                "onset_date": "2024-01-12",
                "symptoms": "Cough, fever, chest pain, dyspnea",
                "body_site": "Right lower lobe",
                "treatment_plan": "Antibiotic therapy, supportive care",
                "requires_followup": True,
                "followup_date": "2024-01-22"
            }
        }


# Update Schema
class DiagnosisUpdate(BaseModel):
    """Schema for updating diagnosis"""
    diagnosis_name: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = Field(None, min_length=5)
    diagnosis_type: Optional[DiagnosisType] = None
    category: Optional[str] = None
    severity: Optional[DiagnosisSeverity] = None
    status: Optional[DiagnosisStatus] = None
    symptoms: Optional[str] = None
    clinical_findings: Optional[str] = None
    body_site: Optional[str] = None
    laterality: Optional[Laterality] = None
    stage: Optional[str] = None
    grade: Optional[str] = None
    is_confirmed: Optional[bool] = None
    confirmed_by: Optional[str] = None
    confirmed_date: Optional[str] = None
    confirmation_method: Optional[ConfirmationMethod] = None
    treatment_plan: Optional[str] = None
    prognosis: Optional[Prognosis] = None
    expected_outcome: Optional[str] = None
    resolution_date: Optional[str] = None
    requires_followup: Optional[bool] = None
    followup_date: Optional[str] = None
    complications: Optional[str] = None
    management_plan: Optional[str] = None
    priority: Optional[Priority] = None
    notes: Optional[str] = None
    internal_notes: Optional[str] = None

    @field_validator('confirmed_date', 'resolution_date', 'followup_date')
    @classmethod
    def validate_date(cls, v):
        if v is None:
            return None
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")


# Response Schema
class DiagnosisResponse(DiagnosisBase):
    """Schema for diagnosis response"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    # Calculated fields
    days_since_diagnosis: Optional[int] = Field(None, description="Days since diagnosed")
    days_since_onset: Optional[int] = Field(None, description="Days since onset")
    is_recent: bool = Field(default=False, description="Diagnosed within last 7 days")
    
    model_config = ConfigDict(from_attributes=True)
    
    @model_validator(mode='after')
    def calculate_durations(self):
        """Calculate time-based fields"""
        if self.diagnosis_date:
            diagnosis_dt = datetime.strptime(self.diagnosis_date, '%Y-%m-%d')
            self.days_since_diagnosis = (datetime.now() - diagnosis_dt).days
            self.is_recent = self.days_since_diagnosis <= 7
        
        if self.onset_date:
            onset_dt = datetime.strptime(self.onset_date, '%Y-%m-%d')
            self.days_since_onset = (datetime.now() - onset_dt).days
        
        return self
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "diagnosis_code": "DX-2024-0001",
                "diagnosis_name": "Community-acquired pneumonia",
                "icd_code": "J18.9",
                "icd_version": "ICD-10",
                "patient_id": 123,
                "doctor_id": 45,
                "diagnosis_type": "primary",
                "severity": "moderate",
                "status": "active",
                "diagnosis_date": "2024-01-15",
                "days_since_diagnosis": 2,
                "is_recent": True,
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00"
            }
        }


# Detailed Response with Relationships
class DiagnosisDetailResponse(DiagnosisResponse):
    """Detailed diagnosis with relationships"""
    patient: Optional[PatientBasic] = None
    doctor: Optional[DoctorBasic] = None
    
    # Parsed complex fields
    differential_diagnoses_detail: Optional[List[DifferentialDiagnosis]] = None
    clinical_findings_detail: Optional[List[ClinicalFinding]] = None
    medications_detail: Optional[List[Medication]] = None
    procedures_detail: Optional[List[Procedure]] = None
    risk_factors_detail: Optional[List[RiskFactor]] = None
    comorbidities_detail: Optional[List[Comorbidity]] = None
    
    model_config = ConfigDict(from_attributes=True)


# List Response Schema
class DiagnosisListResponse(BaseModel):
    """Schema for paginated list of diagnoses"""
    total: int = Field(..., description="Total number of records")
    page: int = Field(..., ge=1, description="Current page number")
    page_size: int = Field(..., ge=1, le=100, description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")
    items: List[DiagnosisResponse] = Field(..., description="Diagnosis items")
    summary: Optional[Dict[str, Any]] = Field(None, description="Summary statistics")


# Filter Schema
class DiagnosisFilter(BaseModel):
    """Schema for filtering diagnoses"""
    # ID filters
    patient_id: Optional[int] = Field(None, description="Filter by patient ID")
    doctor_id: Optional[int] = Field(None, description="Filter by doctor ID")
    admission_id: Optional[int] = Field(None, description="Filter by admission ID")
    appointment_id: Optional[int] = Field(None, description="Filter by appointment ID")
    
    # Code filters
    icd_code: Optional[str] = Field(None, description="Filter by ICD code")
    icd_version: Optional[ICDVersion] = Field(None, description="Filter by ICD version")
    category: Optional[str] = Field(None, description="Filter by category")
    
    # Type/Status filters
    diagnosis_type: Optional[Union[DiagnosisType, List[DiagnosisType]]] = None
    severity: Optional[Union[DiagnosisSeverity, List[DiagnosisSeverity]]] = None
    status: Optional[Union[DiagnosisStatus, List[DiagnosisStatus]]] = None
    prognosis: Optional[Prognosis] = None
    priority: Optional[Priority] = None
    
    # Boolean filters
    is_confirmed: Optional[bool] = None
    is_chronic: Optional[bool] = None
    requires_followup: Optional[bool] = None
    is_notifiable: Optional[bool] = None
    
    # Date filters
    diagnosis_date_from: Optional[str] = None
    diagnosis_date_to: Optional[str] = None
    onset_date_from: Optional[str] = None
    onset_date_to: Optional[str] = None
    
    # Anatomical filters
    body_site: Optional[str] = None
    laterality: Optional[Laterality] = None
    
    # Search
    search: Optional[str] = Field(None, description="Search in diagnosis name, description")
    
    # Pagination
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")
    
    # Sorting
    sort_by: Optional[str] = Field("diagnosis_date", description="Field to sort by")
    sort_order: Optional[str] = Field("desc", pattern="^(asc|desc)$", description="Sort order")
    
    # Include relationships
    include_patient: bool = Field(False, description="Include patient details")
    include_doctor: bool = Field(False, description="Include doctor details")

    @field_validator('diagnosis_date_from', 'diagnosis_date_to', 'onset_date_from', 'onset_date_to')
    @classmethod
    def validate_date(cls, v):
        if v is None:
            return None
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")


# Confirm Diagnosis Schema
class ConfirmDiagnosis(BaseModel):
    """Schema for confirming diagnosis"""
    confirmed_by: str = Field(..., description="Confirming physician")
    confirmed_date: Optional[str] = Field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d'))
    confirmation_method: ConfirmationMethod = Field(..., description="Confirmation method")
    lab_results: Optional[List[int]] = Field(None, description="Supporting lab test IDs")
    imaging_results: Optional[List[int]] = Field(None, description="Supporting imaging IDs")
    notes: Optional[str] = Field(None, description="Confirmation notes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "confirmed_by": "Dr. John Smith",
                "confirmed_date": "2024-01-16",
                "confirmation_method": "imaging",
                "imaging_results": [123, 124],
                "notes": "Chest X-ray confirms right lower lobe infiltrate consistent with pneumonia"
            }
        }


# Resolve Diagnosis Schema
class ResolveDiagnosis(BaseModel):
    """Schema for resolving/closing diagnosis"""
    resolution_date: str = Field(..., description="Resolution date")
    resolution_notes: str = Field(..., min_length=10, description="Resolution notes")
    outcome: str = Field(..., description="Final outcome")
    resolved_by: str = Field(..., description="Resolving physician")
    complications: Optional[str] = Field(None, description="Any complications")
    
    @field_validator('resolution_date')
    @classmethod
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
    
    class Config:
        json_schema_extra = {
            "example": {
                "resolution_date": "2024-01-22",
                "resolution_notes": "Patient completed 7-day antibiotic course. Symptoms fully resolved. Repeat chest X-ray shows clearing of infiltrate.",
                "outcome": "Complete recovery without complications",
                "resolved_by": "Dr. John Smith",
                "complications": "None"
            }
        }


# Statistics Schema
class DiagnosisStats(BaseModel):
    """Diagnosis statistics"""
    total_diagnoses: int
    active_diagnoses: int
    resolved_diagnoses: int
    chronic_diagnoses: int
    confirmed_diagnoses: int
    
    # By type
    diagnoses_by_type: Dict[str, int]
    diagnoses_by_severity: Dict[str, int]
    diagnoses_by_status: Dict[str, int]
    diagnoses_by_category: Dict[str, int]
    
    # Top diagnoses
    top_icd_codes: List[Dict[str, Any]] = Field(..., description="Most common ICD codes")
    top_categories: List[Dict[str, Any]] = Field(..., description="Most common categories")
    
    # Time-based
    diagnoses_today: int
    diagnoses_this_week: int
    diagnoses_this_month: int
    
    # Trends
    trend_by_month: Optional[List[Dict[str, Any]]] = None
    
    # Chronic disease management
    chronic_conditions_count: int
    patients_with_chronic: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_diagnoses": 5000,
                "active_diagnoses": 1200,
                "resolved_diagnoses": 3500,
                "chronic_diagnoses": 800,
                "confirmed_diagnoses": 4200,
                "diagnoses_by_type": {
                    "primary": 3000,
                    "secondary": 1500,
                    "differential": 500
                },
                "diagnoses_by_severity": {
                    "mild": 2000,
                    "moderate": 2000,
                    "severe": 800,
                    "critical": 200
                },
                "diagnoses_by_status": {
                    "active": 1200,
                    "resolved": 3500,
                    "chronic": 300
                },
                "diagnoses_by_category": {
                    "Respiratory": 800,
                    "Cardiovascular": 600,
                    "Infectious": 500
                },
                "top_icd_codes": [
                    {"code": "J18.9", "description": "Pneumonia", "count": 150},
                    {"code": "E11.9", "description": "Type 2 Diabetes", "count": 120}
                ],
                "top_categories": [
                    {"category": "Respiratory", "count": 800},
                    {"category": "Cardiovascular", "count": 600}
                ],
                "diagnoses_today": 25,
                "diagnoses_this_week": 150,
                "diagnoses_this_month": 600,
                "chronic_conditions_count": 800,
                "patients_with_chronic": 450
            }
        }


# ICD Code Lookup Schema
class ICDCodeLookup(BaseModel):
    """ICD code lookup request"""
    search_term: str = Field(..., min_length=2, description="Search term")
    icd_version: ICDVersion = Field(default=ICDVersion.ICD_10)
    category: Optional[str] = None
    limit: int = Field(20, ge=1, le=100)
    
    class Config:
        json_schema_extra = {
            "example": {
                "search_term": "pneumonia",
                "icd_version": "ICD-10",
                "limit": 20
            }
        }


class ICDCodeResult(BaseModel):
    """ICD code search result"""
    code: str
    description: str
    category: Optional[str] = None
    billable: bool = Field(default=True)
    icd_version: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": "J18.9",
                "description": "Pneumonia, unspecified organism",
                "category": "Diseases of the respiratory system",
                "billable": True,
                "icd_version": "ICD-10"
            }
        }


# Patient Diagnosis History Schema
class PatientDiagnosisHistory(BaseModel):
    """Patient's diagnosis history"""
    patient_id: int
    patient_name: str
    total_diagnoses: int
    active_diagnoses: int
    chronic_conditions: int
    recent_diagnoses: List[DiagnosisResponse]
    chronic_diagnoses: List[DiagnosisResponse]
    diagnosis_timeline: List[Dict[str, Any]]
    
    class Config:
        json_schema_extra = {
            "example": {
                "patient_id": 123,
                "patient_name": "John Doe",
                "total_diagnoses": 15,
                "active_diagnoses": 3,
                "chronic_conditions": 2,
                "recent_diagnoses": [],
                "chronic_diagnoses": [],
                "diagnosis_timeline": [
                    {"date": "2024-01-15", "diagnosis": "Pneumonia", "status": "active"},
                    {"date": "2023-06-10", "diagnosis": "Hypertension", "status": "chronic"}
                ]
            }
        }


# Export Schema
class DiagnosisExport(BaseModel):
    """Export diagnoses"""
    filters: DiagnosisFilter
    export_format: str = Field(..., pattern="^(csv|xlsx|pdf|json)$")
    include_details: bool = Field(default=False)
    filename: Optional[str] = None


# Bulk Operations
class DiagnosisBulkStatusUpdate(BaseModel):
    """Bulk update diagnosis status"""
    diagnosis_ids: List[int] = Field(..., min_length=1, max_length=50)
    status: DiagnosisStatus
    notes: Optional[str] = None
    
    @field_validator('diagnosis_ids')
    @classmethod
    def validate_ids(cls, v):
        if len(v) > 50:
            raise ValueError("Cannot update more than 50 diagnoses at once")
        return v