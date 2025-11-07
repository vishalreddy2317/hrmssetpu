"""
Imaging Schemas
Pydantic schemas for radiology and medical imaging services
"""

from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from typing import Optional, List, Dict, Any, Union
from datetime import datetime, date, time, timedelta
from decimal import Decimal
from enum import Enum
import json
import re


# Enums
class ImagingType(str, Enum):
    """Medical imaging modalities"""
    XRAY = "xray"
    CT_SCAN = "ct_scan"
    MRI = "mri"
    ULTRASOUND = "ultrasound"
    MAMMOGRAPHY = "mammography"
    PET_SCAN = "pet_scan"
    FLUOROSCOPY = "fluoroscopy"
    DEXA_SCAN = "dexa_scan"
    ECHOCARDIOGRAM = "echocardiogram"
    ANGIOGRAPHY = "angiography"
    NUCLEAR_MEDICINE = "nuclear_medicine"


class ImagingPriority(str, Enum):
    """Priority levels"""
    STAT = "stat"  # Immediate
    URGENT = "urgent"  # Within hours
    ROUTINE = "routine"  # Scheduled


class ImagingStatus(str, Enum):
    """Imaging study status"""
    PENDING = "pending"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REPORTED = "reported"
    VERIFIED = "verified"


class ImageQuality(str, Enum):
    """Image quality assessment"""
    EXCELLENT = "excellent"
    GOOD = "good"
    ADEQUATE = "adequate"
    POOR = "poor"
    REPEAT_REQUIRED = "repeat_required"


class BodyRegion(str, Enum):
    """Common body regions"""
    HEAD = "head"
    NECK = "neck"
    CHEST = "chest"
    ABDOMEN = "abdomen"
    PELVIS = "pelvis"
    SPINE = "spine"
    UPPER_EXTREMITY = "upper_extremity"
    LOWER_EXTREMITY = "lower_extremity"
    HEART = "heart"
    BREAST = "breast"


class ContrastType(str, Enum):
    """Types of contrast agents"""
    IODINATED = "iodinated"
    GADOLINIUM = "gadolinium"
    BARIUM = "barium"
    AIR = "air"
    MICROBUBBLES = "microbubbles"


# Helper Schemas
class PatientBasic(BaseModel):
    """Basic patient information"""
    id: int
    full_name: str
    patient_number: Optional[str] = None
    date_of_birth: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    
    class Config:
        from_attributes = True


class DoctorBasic(BaseModel):
    """Basic doctor information"""
    id: int
    full_name: str
    specialization: Optional[str] = None
    license_number: Optional[str] = None
    
    class Config:
        from_attributes = True


class StaffBasic(BaseModel):
    """Basic staff/technician information"""
    id: int
    name: str
    designation: Optional[str] = None
    department: Optional[str] = None
    
    class Config:
        from_attributes = True


class ContrastInfo(BaseModel):
    """Contrast agent information"""
    contrast_used: bool = Field(..., description="Whether contrast was used")
    contrast_type: Optional[ContrastType] = Field(None, description="Type of contrast")
    contrast_amount: Optional[str] = Field(None, max_length=50, description="Amount administered")
    administration_route: Optional[str] = Field(None, description="IV, oral, rectal, etc.")
    adverse_reaction: bool = Field(default=False, description="Any adverse reaction")
    reaction_details: Optional[str] = Field(None, description="Reaction details if any")
    
    class Config:
        json_schema_extra = {
            "example": {
                "contrast_used": True,
                "contrast_type": "iodinated",
                "contrast_amount": "100 ml",
                "administration_route": "Intravenous",
                "adverse_reaction": False
            }
        }


class RadiationDose(BaseModel):
    """Radiation dose information"""
    dose_length_product: Optional[str] = Field(None, description="DLP (mGy·cm)")
    ctdi_vol: Optional[str] = Field(None, description="CTDIvol (mGy)")
    effective_dose: Optional[str] = Field(None, description="Effective dose (mSv)")
    exposure_time: Optional[str] = Field(None, description="Exposure time")
    
    class Config:
        json_schema_extra = {
            "example": {
                "dose_length_product": "500 mGy·cm",
                "ctdi_vol": "15 mGy",
                "effective_dose": "7.5 mSv",
                "exposure_time": "2.5 seconds"
            }
        }


class ImagingFindings(BaseModel):
    """Structured imaging findings"""
    findings: str = Field(..., min_length=10, description="Detailed findings")
    impression: str = Field(..., min_length=10, description="Radiologist impression/conclusion")
    recommendations: Optional[str] = Field(None, description="Follow-up recommendations")
    is_abnormal: bool = Field(default=False, description="Abnormal findings present")
    critical_findings: Optional[str] = Field(None, description="Critical/urgent findings")
    comparison: Optional[str] = Field(None, description="Comparison with previous studies")
    
    class Config:
        json_schema_extra = {
            "example": {
                "findings": "The lung fields are clear. No focal consolidation, pleural effusion, or pneumothorax. Heart size is normal. Mediastinal contours are unremarkable.",
                "impression": "Normal chest radiograph. No acute cardiopulmonary process.",
                "recommendations": "No immediate follow-up required. Clinical correlation advised.",
                "is_abnormal": False,
                "critical_findings": None,
                "comparison": "Compared to previous study dated 2023-12-01, no significant interval change."
            }
        }


class ImageMetadata(BaseModel):
    """Individual image metadata"""
    image_url: str = Field(..., description="Image file URL")
    sequence_number: int = Field(..., description="Image sequence number")
    view: Optional[str] = Field(None, description="AP, PA, Lateral, Oblique, etc.")
    window_level: Optional[str] = Field(None, description="Window/level settings")
    file_format: str = Field(default="DICOM", description="Image format")
    file_size_mb: Optional[float] = Field(None, description="File size in MB")
    
    class Config:
        json_schema_extra = {
            "example": {
                "image_url": "https://pacs.hospital.com/images/study123/image001.dcm",
                "sequence_number": 1,
                "view": "PA",
                "window_level": "Lung window",
                "file_format": "DICOM",
                "file_size_mb": 2.5
            }
        }


class DICOMMetadata(BaseModel):
    """DICOM study metadata"""
    study_instance_uid: str = Field(..., description="DICOM Study Instance UID")
    series_instance_uid: Optional[str] = Field(None, description="Series Instance UID")
    accession_number: Optional[str] = Field(None, description="Accession number")
    study_date: Optional[str] = Field(None, description="DICOM study date")
    study_time: Optional[str] = Field(None, description="DICOM study time")
    modality: str = Field(..., description="DICOM modality (CR, CT, MR, US, etc.)")
    station_name: Optional[str] = Field(None, description="Acquisition device station")
    manufacturer: Optional[str] = Field(None, description="Equipment manufacturer")
    model: Optional[str] = Field(None, description="Equipment model")
    
    class Config:
        json_schema_extra = {
            "example": {
                "study_instance_uid": "1.2.840.113619.2.55.3.604688119.456.1234567890.123",
                "series_instance_uid": "1.2.840.113619.2.55.3.604688119.456.1234567890.124",
                "accession_number": "ACC123456",
                "study_date": "20240115",
                "study_time": "143022",
                "modality": "CT",
                "station_name": "CT-SCANNER-01",
                "manufacturer": "GE Healthcare",
                "model": "Revolution CT"
            }
        }


class PatientPreparation(BaseModel):
    """Patient preparation instructions"""
    preparation_instructions: str = Field(..., description="Preparation instructions")
    fasting_required: bool = Field(default=False, description="Fasting required")
    fasting_hours: Optional[int] = Field(None, ge=0, le=24, description="Hours of fasting")
    hydration_required: bool = Field(default=False, description="Hydration required")
    medication_restrictions: Optional[str] = Field(None, description="Medication restrictions")
    arrival_time: Optional[str] = Field(None, description="When to arrive before appointment")
    bring_items: Optional[List[str]] = Field(None, description="Items to bring")
    
    class Config:
        json_schema_extra = {
            "example": {
                "preparation_instructions": "Please fast for 6 hours before the procedure. Drink plenty of water. Bring previous imaging CDs if available.",
                "fasting_required": True,
                "fasting_hours": 6,
                "hydration_required": True,
                "medication_restrictions": "Continue all medications except Metformin",
                "arrival_time": "30 minutes before appointment",
                "bring_items": ["Previous imaging CDs", "Insurance card", "Photo ID"]
            }
        }


# Base Schema
class ImagingBase(BaseModel):
    """Base schema for imaging studies"""
    imaging_number: str = Field(..., max_length=20, description="Unique imaging identifier")
    
    # Patient and Ordering
    patient_id: int = Field(..., description="Patient ID")
    ordered_by_doctor_id: int = Field(..., description="Ordering physician ID")
    
    # Imaging Details
    imaging_type: ImagingType = Field(..., description="Type of imaging")
    body_part: str = Field(..., max_length=100, description="Body part/region")
    study_description: str = Field(..., max_length=200, description="Study description")
    modality: Optional[str] = Field(None, max_length=50, description="DICOM modality code")
    
    # Scheduling
    order_date: str = Field(..., description="Order date (YYYY-MM-DD)")
    order_time: str = Field(..., pattern="^([01][0-9]|2[0-3]):[0-5][0-9]$", description="Order time (HH:MM)")
    scheduled_date: Optional[str] = Field(None, description="Scheduled date")
    scheduled_time: Optional[str] = Field(None, pattern="^([01][0-9]|2[0-3]):[0-5][0-9]$")
    
    # Actual Performance
    actual_date: Optional[str] = Field(None, description="Actual date performed")
    actual_time: Optional[str] = Field(None, pattern="^([01][0-9]|2[0-3]):[0-5][0-9]$")
    
    # Priority and Status
    priority: ImagingPriority = Field(default=ImagingPriority.ROUTINE)
    status: ImagingStatus = Field(default=ImagingStatus.PENDING)
    
    # Clinical Information
    clinical_indication: str = Field(..., min_length=10, description="Clinical indication for study")
    relevant_history: Optional[str] = Field(None, description="Relevant clinical history")
    
    # Personnel
    performed_by: Optional[str] = Field(None, max_length=200, description="Technician name")
    technician_id: Optional[int] = Field(None, description="Technician staff ID")
    radiologist_id: Optional[int] = Field(None, description="Reporting radiologist ID")
    reported_by: Optional[str] = Field(None, max_length=200, description="Radiologist name")
    report_date: Optional[str] = Field(None, description="Report date")
    
    # Findings
    findings: Optional[str] = Field(None, description="Radiologist findings")
    impression: Optional[str] = Field(None, description="Impression/conclusion")
    recommendations: Optional[str] = Field(None, description="Recommendations")
    
    # Contrast
    contrast_used: bool = Field(default=False)
    contrast_type: Optional[str] = Field(None, max_length=100)
    contrast_amount: Optional[str] = Field(None, max_length=50)
    
    # Radiation (for X-ray, CT)
    radiation_dose: Optional[str] = Field(None, max_length=50)
    
    # Images
    image_count: Optional[int] = Field(None, ge=0, description="Number of images")
    images_urls: Optional[List[str]] = Field(None, description="Image URLs")
    dicom_study_id: Optional[str] = Field(None, max_length=100, description="DICOM Study UID")
    
    # Report
    report_url: Optional[str] = Field(None, max_length=500)
    is_abnormal: bool = Field(default=False)
    
    # Cost
    cost: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    
    # Location
    imaging_center: Optional[str] = Field(None, max_length=200)
    imaging_floor: Optional[int] = Field(None, description="Floor number")
    
    # Patient Preparation
    preparation_instructions: Optional[str] = Field(None)
    fasting_required: bool = Field(default=False)
    
    # Quality
    image_quality: Optional[ImageQuality] = Field(None)
    
    # Notes
    notes: Optional[str] = Field(None)
    technician_notes: Optional[str] = Field(None)

    @field_validator('order_date', 'scheduled_date', 'actual_date', 'report_date')
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
    
    @field_validator('images_urls', mode='before')
    @classmethod
    def parse_images_urls(cls, v):
        """Parse image URLs if JSON string"""
        if v is None:
            return None
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                raise ValueError("Images URLs must be valid JSON array")
        return v
    
    @model_validator(mode='after')
    def validate_dates_chronology(self):
        """Validate chronological order of dates"""
        if self.scheduled_date and self.order_date:
            scheduled = datetime.strptime(self.scheduled_date, '%Y-%m-%d')
            ordered = datetime.strptime(self.order_date, '%Y-%m-%d')
            if scheduled < ordered:
                raise ValueError("Scheduled date cannot be before order date")
        
        if self.actual_date and self.scheduled_date:
            actual = datetime.strptime(self.actual_date, '%Y-%m-%d')
            scheduled = datetime.strptime(self.scheduled_date, '%Y-%m-%d')
            # Actual can be different day if rescheduled, so just warn
        
        return self
    
    @model_validator(mode='after')
    def validate_reported_status(self):
        """Validate reporting fields consistency"""
        if self.status == ImagingStatus.REPORTED:
            if not self.findings or not self.impression:
                raise ValueError("Findings and impression required when status is reported")
            if not self.radiologist_id:
                raise ValueError("Radiologist ID required when status is reported")
        return self


# Create Schema
class ImagingCreate(BaseModel):
    """Schema for creating imaging study"""
    # Patient and ordering
    patient_id: int
    ordered_by_doctor_id: int
    
    # Study details
    imaging_type: ImagingType
    body_part: str = Field(..., max_length=100)
    study_description: str = Field(..., max_length=200)
    modality: Optional[str] = None
    
    # Scheduling
    order_date: Optional[str] = Field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d'))
    order_time: Optional[str] = Field(default_factory=lambda: datetime.now().strftime('%H:%M'))
    scheduled_date: Optional[str] = None
    scheduled_time: Optional[str] = None
    
    # Priority
    priority: ImagingPriority = Field(default=ImagingPriority.ROUTINE)
    
    # Clinical info
    clinical_indication: str = Field(..., min_length=10)
    relevant_history: Optional[str] = None
    
    # Preparation
    preparation: Optional[PatientPreparation] = None
    
    # Cost
    cost: Optional[Decimal] = Field(None, ge=0)
    
    # Location
    imaging_center: Optional[str] = None
    imaging_floor: Optional[int] = None
    
    # Notes
    notes: Optional[str] = None
    
    # Auto-generated
    imaging_number: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "patient_id": 123,
                "ordered_by_doctor_id": 45,
                "imaging_type": "ct_scan",
                "body_part": "Abdomen",
                "study_description": "CT Abdomen and Pelvis with Contrast",
                "modality": "CT",
                "priority": "urgent",
                "clinical_indication": "Acute abdominal pain, rule out appendicitis",
                "relevant_history": "Patient has history of previous abdominal surgery",
                "scheduled_date": "2024-01-16",
                "scheduled_time": "14:00",
                "cost": 850.00,
                "imaging_center": "Radiology Department - Main Building",
                "imaging_floor": 2
            }
        }


# Update Schema
class ImagingUpdate(BaseModel):
    """Schema for updating imaging study"""
    scheduled_date: Optional[str] = None
    scheduled_time: Optional[str] = None
    actual_date: Optional[str] = None
    actual_time: Optional[str] = None
    status: Optional[ImagingStatus] = None
    priority: Optional[ImagingPriority] = None
    performed_by: Optional[str] = None
    technician_id: Optional[int] = None
    contrast_used: Optional[bool] = None
    contrast_type: Optional[str] = None
    contrast_amount: Optional[str] = None
    radiation_dose: Optional[str] = None
    image_count: Optional[int] = None
    image_quality: Optional[ImageQuality] = None
    technician_notes: Optional[str] = None
    notes: Optional[str] = None


# Response Schema
class ImagingResponse(ImagingBase):
    """Schema for imaging response"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    # Calculated fields
    days_since_order: Optional[int] = Field(None, description="Days since ordered")
    days_to_scheduled: Optional[int] = Field(None, description="Days until scheduled")
    is_overdue: bool = Field(default=False, description="Past scheduled date")
    is_urgent: bool = Field(default=False, description="STAT or urgent priority")
    turnaround_time_hours: Optional[int] = Field(None, description="Order to report time")
    has_report: bool = Field(default=False, description="Report available")
    has_images: bool = Field(default=False, description="Images available")
    
    model_config = ConfigDict(from_attributes=True)
    
    @model_validator(mode='after')
    def calculate_fields(self):
        """Calculate additional fields"""
        # Days since order
        if self.order_date:
            order_dt = datetime.strptime(self.order_date, '%Y-%m-%d')
            self.days_since_order = (datetime.now() - order_dt).days
        
        # Days to scheduled
        if self.scheduled_date:
            scheduled_dt = datetime.strptime(self.scheduled_date, '%Y-%m-%d')
            delta = (scheduled_dt - datetime.now()).days
            self.days_to_scheduled = delta
            self.is_overdue = delta < 0 and self.status not in [ImagingStatus.COMPLETED, ImagingStatus.REPORTED, ImagingStatus.CANCELLED]
        
        # Priority flags
        self.is_urgent = self.priority in [ImagingPriority.STAT, ImagingPriority.URGENT]
        
        # Turnaround time
        if self.order_date and self.report_date:
            order_dt = datetime.strptime(f"{self.order_date} {self.order_time}", '%Y-%m-%d %H:%M')
            report_dt = datetime.strptime(self.report_date, '%Y-%m-%d')
            delta = report_dt - order_dt
            self.turnaround_time_hours = int(delta.total_seconds() / 3600)
        
        # Availability flags
        self.has_report = self.report_url is not None or self.findings is not None
        self.has_images = bool(self.images_urls and len(self.images_urls) > 0)
        
        return self
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "imaging_number": "IMG-2024-0001",
                "patient_id": 123,
                "imaging_type": "ct_scan",
                "body_part": "Abdomen",
                "study_description": "CT Abdomen and Pelvis with Contrast",
                "priority": "urgent",
                "status": "completed",
                "order_date": "2024-01-15",
                "scheduled_date": "2024-01-16",
                "actual_date": "2024-01-16",
                "is_abnormal": False,
                "has_report": True,
                "has_images": True,
                "days_since_order": 2,
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-16T15:00:00"
            }
        }


# Detail Response with Relationships
class ImagingDetailResponse(ImagingResponse):
    """Detailed imaging with relationships"""
    patient: Optional[PatientBasic] = None
    ordered_by: Optional[DoctorBasic] = None
    radiologist: Optional[DoctorBasic] = None
    technician: Optional[StaffBasic] = None
    
    # Enhanced details
    contrast_info: Optional[ContrastInfo] = None
    radiation_info: Optional[RadiationDose] = None
    dicom_metadata: Optional[DICOMMetadata] = None
    image_list: Optional[List[ImageMetadata]] = None
    
    model_config = ConfigDict(from_attributes=True)


# List Response Schema
class ImagingListResponse(BaseModel):
    """Schema for paginated list of imaging studies"""
    total: int = Field(..., description="Total number of records")
    page: int = Field(..., ge=1, description="Current page number")
    page_size: int = Field(..., ge=1, le=100, description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")
    items: List[ImagingResponse] = Field(..., description="Imaging items")
    summary: Optional[Dict[str, Any]] = Field(None, description="Summary statistics")


# Filter Schema
class ImagingFilter(BaseModel):
    """Schema for filtering imaging studies"""
    # ID filters
    patient_id: Optional[int] = Field(None, description="Filter by patient ID")
    ordered_by_doctor_id: Optional[int] = Field(None, description="Filter by ordering doctor")
    radiologist_id: Optional[int] = Field(None, description="Filter by radiologist")
    technician_id: Optional[int] = Field(None, description="Filter by technician")
    
    # String filters
    imaging_number: Optional[str] = Field(None, description="Filter by imaging number")
    dicom_study_id: Optional[str] = Field(None, description="Filter by DICOM study ID")
    body_part: Optional[str] = Field(None, description="Filter by body part")
    
    # Type filters
    imaging_type: Optional[Union[ImagingType, List[ImagingType]]] = Field(None, description="Filter by type")
    status: Optional[Union[ImagingStatus, List[ImagingStatus]]] = Field(None, description="Filter by status")
    priority: Optional[ImagingPriority] = Field(None, description="Filter by priority")
    image_quality: Optional[ImageQuality] = Field(None, description="Filter by quality")
    
    # Boolean filters
    is_abnormal: Optional[bool] = Field(None, description="Abnormal findings only")
    contrast_used: Optional[bool] = Field(None, description="Studies with contrast")
    has_report: Optional[bool] = Field(None, description="Has report")
    has_images: Optional[bool] = Field(None, description="Has images")
    
    # Date filters
    order_date_from: Optional[str] = Field(None, description="Ordered from date")
    order_date_to: Optional[str] = Field(None, description="Ordered to date")
    scheduled_date_from: Optional[str] = Field(None, description="Scheduled from date")
    scheduled_date_to: Optional[str] = Field(None, description="Scheduled to date")
    actual_date_from: Optional[str] = Field(None, description="Performed from date")
    actual_date_to: Optional[str] = Field(None, description="Performed to date")
    
    # Special filters
    stat_urgent_only: Optional[bool] = Field(None, description="STAT and urgent only")
    pending_report: Optional[bool] = Field(None, description="Awaiting report")
    today_scheduled: Optional[bool] = Field(None, description="Scheduled for today")
    overdue: Optional[bool] = Field(None, description="Overdue studies")
    
    # Search
    search: Optional[str] = Field(None, description="Search in description, indication, findings")
    
    # Pagination
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")
    
    # Sorting
    sort_by: str = Field("order_date", description="Field to sort by")
    sort_order: str = Field("desc", pattern="^(asc|desc)$", description="Sort order")
    
    # Include relationships
    include_patient: bool = Field(False, description="Include patient details")
    include_doctors: bool = Field(False, description="Include doctor details")
    include_technician: bool = Field(False, description="Include technician details")
    include_images: bool = Field(False, description="Include image list")

    @field_validator('order_date_from', 'order_date_to', 'scheduled_date_from', 
                     'scheduled_date_to', 'actual_date_from', 'actual_date_to')
    @classmethod
    def validate_date(cls, v):
        if v is None:
            return None
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")


# Schedule Imaging Schema
class ScheduleImaging(BaseModel):
    """Schema for scheduling imaging study"""
    scheduled_date: str = Field(..., description="Scheduled date (YYYY-MM-DD)")
    scheduled_time: str = Field(..., pattern="^([01][0-9]|2[0-3]):[0-5][0-9]$")
    imaging_center: Optional[str] = Field(None, max_length=200)
    imaging_floor: Optional[int] = None
    technician_id: Optional[int] = None
    preparation_instructions: Optional[str] = None
    send_reminder: bool = Field(default=True, description="Send appointment reminder")
    
    @field_validator('scheduled_date')
    @classmethod
    def validate_date(cls, v):
        try:
            scheduled = datetime.strptime(v, '%Y-%m-%d')
            if scheduled.date() < datetime.now().date():
                raise ValueError("Scheduled date cannot be in the past")
            return v
        except ValueError as e:
            if "does not match format" in str(e):
                raise ValueError("Date must be in YYYY-MM-DD format")
            raise
    
    class Config:
        json_schema_extra = {
            "example": {
                "scheduled_date": "2024-01-20",
                "scheduled_time": "10:30",
                "imaging_center": "Radiology Department - Main Building",
                "imaging_floor": 2,
                "preparation_instructions": "Fast for 6 hours before the procedure",
                "send_reminder": True
            }
        }


# Complete Study Schema
class CompleteStudy(BaseModel):
    """Schema for completing imaging study"""
    actual_date: str = Field(..., description="Date performed")
    actual_time: str = Field(..., description="Time performed")
    performed_by: str = Field(..., max_length=200)
    technician_id: Optional[int] = None
    
    # Images
    image_count: int = Field(..., ge=1, description="Number of images acquired")
    images_urls: Optional[List[str]] = Field(None, description="Image URLs")
    dicom_study_id: Optional[str] = None
    
    # Contrast
    contrast_used: bool = Field(default=False)
    contrast_info: Optional[ContrastInfo] = None
    
    # Radiation
    radiation_dose: Optional[str] = None
    
    # Quality
    image_quality: ImageQuality = Field(..., description="Image quality assessment")
    
    # Notes
    technician_notes: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "actual_date": "2024-01-16",
                "actual_time": "14:30",
                "performed_by": "John Smith, RT",
                "technician_id": 67,
                "image_count": 150,
                "dicom_study_id": "1.2.840.113619.2.55.3.604688119.456.1234567890.123",
                "contrast_used": True,
                "contrast_info": {
                    "contrast_used": True,
                    "contrast_type": "iodinated",
                    "contrast_amount": "100 ml",
                    "administration_route": "IV",
                    "adverse_reaction": False
                },
                "image_quality": "excellent",
                "technician_notes": "Patient cooperative. No issues during scan."
            }
        }


# Add Report Schema
class AddReport(BaseModel):
    """Schema for adding radiology report"""
    radiologist_id: int = Field(..., description="Reporting radiologist ID")
    reported_by: str = Field(..., max_length=200, description="Radiologist name")
    report_date: Optional[str] = Field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d'))
    
    # Findings
    findings: ImagingFindings = Field(..., description="Structured findings")
    
    # Report document
    report_url: Optional[str] = Field(None, description="URL to formatted report PDF")
    
    # Additional info
    comparison_studies: Optional[List[int]] = Field(None, description="IDs of comparison studies")
    
    @field_validator('report_date')
    @classmethod
    def validate_date(cls, v):
        if v:
            try:
                datetime.strptime(v, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Date must be in YYYY-MM-DD format")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "radiologist_id": 89,
                "reported_by": "Dr. Sarah Johnson, MD",
                "report_date": "2024-01-16",
                "findings": {
                    "findings": "The lung fields are clear...",
                    "impression": "Normal chest radiograph",
                    "recommendations": "No immediate follow-up required",
                    "is_abnormal": False
                },
                "report_url": "https://reports.hospital.com/rad/IMG-2024-0001.pdf"
            }
        }


# Verify Report Schema
class VerifyReport(BaseModel):
    """Schema for report verification"""
    verified_by: str = Field(..., description="Verifying physician")
    verification_date: Optional[str] = Field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d'))
    verification_notes: Optional[str] = None


# Cancel Study Schema
class CancelStudy(BaseModel):
    """Schema for cancelling imaging study"""
    cancellation_reason: str = Field(..., min_length=10, description="Reason for cancellation")
    cancelled_by: str = Field(..., description="Who cancelled")
    refund_applicable: bool = Field(default=False)
    reschedule: bool = Field(default=False, description="Reschedule for later")
    new_scheduled_date: Optional[str] = Field(None, description="New date if rescheduling")


# Statistics Schema
class ImagingStats(BaseModel):
    """Imaging statistics"""
    total_studies: int
    completed_studies: int
    pending_studies: int
    pending_reports: int
    
    # By type
    studies_by_type: Dict[str, int]
    studies_by_status: Dict[str, int]
    studies_by_priority: Dict[str, int]
    
    # Time-based
    studies_today: int
    studies_this_week: int
    studies_this_month: int
    
    # Performance metrics
    average_turnaround_hours: Optional[float] = Field(None, description="Order to report time")
    same_day_completion_rate: Optional[float] = Field(None, description="Percentage completed same day")
    
    # Quality metrics
    abnormal_findings_rate: Optional[float] = None
    contrast_usage_rate: Optional[float] = None
    average_image_quality: Optional[float] = None
    
    # Modality utilization
    studies_by_modality: Dict[str, int]
    busiest_time_slot: Optional[str] = None
    
    # Top items
    most_common_studies: List[Dict[str, Any]] = Field(default=[])
    top_radiologists: List[Dict[str, Any]] = Field(default=[])
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_studies": 5000,
                "completed_studies": 4500,
                "pending_studies": 300,
                "pending_reports": 200,
                "studies_by_type": {
                    "xray": 2000,
                    "ct_scan": 1500,
                    "mri": 800,
                    "ultrasound": 700
                },
                "studies_by_status": {
                    "completed": 4500,
                    "scheduled": 250,
                    "pending": 150,
                    "reported": 4000
                },
                "studies_by_priority": {
                    "stat": 100,
                    "urgent": 500,
                    "routine": 4400
                },
                "studies_today": 45,
                "studies_this_week": 280,
                "studies_this_month": 1200,
                "average_turnaround_hours": 24.5,
                "same_day_completion_rate": 75.0,
                "abnormal_findings_rate": 35.5,
                "contrast_usage_rate": 25.0,
                "studies_by_modality": {
                    "CR": 2000,
                    "CT": 1500,
                    "MR": 800,
                    "US": 700
                },
                "most_common_studies": [
                    {"study": "Chest X-Ray", "count": 800},
                    {"study": "CT Brain", "count": 500}
                ]
            }
        }


# Dashboard Schema
class ImagingDashboard(BaseModel):
    """Dashboard summary for imaging"""
    today_scheduled: int
    today_completed: int
    pending_today: int
    stat_urgent_pending: int
    pending_reports_count: int
    overdue_count: int
    
    # Current status
    in_progress_now: int
    next_scheduled: Optional[ImagingResponse] = None
    
    # Recent items
    recent_completed: List[ImagingResponse] = Field(default=[], max_length=5)
    urgent_pending: List[ImagingResponse] = Field(default=[], max_length=5)
    
    # Alerts
    alerts: List[str] = Field(default=[])
    
    class Config:
        json_schema_extra = {
            "example": {
                "today_scheduled": 25,
                "today_completed": 18,
                "pending_today": 7,
                "stat_urgent_pending": 3,
                "pending_reports_count": 12,
                "overdue_count": 2,
                "in_progress_now": 2,
                "alerts": [
                    "3 STAT studies pending",
                    "12 reports awaiting radiologist review"
                ]
            }
        }


# Workload Schema
class RadiologistWorkload(BaseModel):
    """Radiologist workload summary"""
    radiologist_id: int
    radiologist_name: str
    
    # Counts
    total_assigned: int
    completed_today: int
    pending_reports: int
    
    # Performance
    average_report_time_minutes: Optional[float] = None
    reports_this_week: int
    reports_this_month: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "radiologist_id": 89,
                "radiologist_name": "Dr. Sarah Johnson",
                "total_assigned": 15,
                "completed_today": 8,
                "pending_reports": 7,
                "average_report_time_minutes": 45.5,
                "reports_this_week": 45,
                "reports_this_month": 180
            }
        }


# PACS Integration Schema
class PACSQuery(BaseModel):
    """PACS query/retrieve request"""
    study_instance_uid: Optional[str] = None
    patient_id: Optional[int] = None
    accession_number: Optional[str] = None
    modality: Optional[str] = None
    study_date_from: Optional[str] = None
    study_date_to: Optional[str] = None


# Export Schema
class ImagingExport(BaseModel):
    """Export imaging data"""
    filters: ImagingFilter
    export_format: str = Field(..., pattern="^(csv|xlsx|pdf|dicom|json)$")
    include_images: bool = Field(default=False)
    include_reports: bool = Field(default=True)
    anonymize: bool = Field(default=False, description="Remove patient identifiers")


# Bulk Operations
class ImagingBulkStatusUpdate(BaseModel):
    """Bulk update status"""
    imaging_ids: List[int] = Field(..., min_length=1, max_length=50)
    status: ImagingStatus
    notes: Optional[str] = None
    
    @field_validator('imaging_ids')
    @classmethod
    def validate_ids(cls, v):
        if len(v) > 50:
            raise ValueError("Cannot update more than 50 studies at once")
        return v


# QA/QC Schema
class QualityControl(BaseModel):
    """Quality control review"""
    imaging_id: int
    reviewed_by: str
    review_date: str
    quality_score: int = Field(..., ge=1, le=5)
    issues_found: Optional[List[str]] = None
    corrective_actions: Optional[str] = None
    approved: bool


# Comparison Study Schema
class ComparisonStudy(BaseModel):
    """Compare with previous studies"""
    current_study_id: int
    previous_study_ids: List[int] = Field(..., min_length=1)
    comparison_notes: str