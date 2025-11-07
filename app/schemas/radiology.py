"""
Radiology Schemas
"""

from pydantic import BaseModel, Field, validator, condecimal
from typing import Optional
from datetime import datetime
from decimal import Decimal


# Base Schema
class RadiologyBase(BaseModel):
    radiology_number: str = Field(..., max_length=20, description="Unique radiology number")
    patient_id: int = Field(..., gt=0)
    doctor_id: int = Field(..., gt=0)
    imaging_type: str = Field(..., max_length=100)
    test_name: str = Field(..., max_length=200)
    body_part: str = Field(..., max_length=100)
    
    @validator('imaging_type')
    def validate_imaging_type(cls, v):
        valid = ['x_ray', 'mri', 'ct_scan', 'ultrasound', 'pet_scan',
                'mammography', 'fluoroscopy', 'bone_scan', 'dexa_scan', 'angiography']
        if v.lower() not in valid:
            raise ValueError(f"Imaging type must be one of: {', '.join(valid)}")
        return v.lower()


# Create Schema
class RadiologyCreate(RadiologyBase):
    test_code: Optional[str] = Field(None, max_length=50)
    category: str = Field(default='diagnostic', max_length=100)
    
    order_date: str = Field(..., max_length=20)
    order_time: str = Field(..., max_length=10)
    
    appointment_id: Optional[int] = None
    scheduled_date: Optional[str] = Field(None, max_length=20)
    scheduled_time: Optional[str] = Field(None, max_length=10)
    
    date_taken: Optional[str] = Field(None, max_length=20)
    time_taken: Optional[str] = Field(None, max_length=10)
    
    # Clinical Information
    clinical_history: Optional[str] = None
    symptoms: Optional[str] = None
    indications: Optional[str] = None
    provisional_diagnosis: Optional[str] = None
    
    # Contrast
    contrast_used: bool = Field(default=False)
    contrast_type: Optional[str] = Field(None, max_length=100)
    contrast_volume: Optional[str] = Field(None, max_length=50)
    
    preparation_required: bool = Field(default=False)
    preparation_instructions: Optional[str] = None
    
    # Staff
    technician_name: Optional[str] = Field(None, max_length=200)
    radiologist_id: Optional[int] = None
    radiologist_name: Optional[str] = Field(None, max_length=200)
    
    # Report
    report_status: str = Field(default='pending', max_length=20)
    findings: Optional[str] = None
    impression: Optional[str] = None
    recommendations: Optional[str] = None
    
    report_date: Optional[str] = Field(None, max_length=20)
    report_time: Optional[str] = Field(None, max_length=10)
    
    result_type: Optional[str] = Field(None, max_length=50)
    
    # Critical
    is_critical: bool = Field(default=False)
    critical_findings: Optional[str] = None
    critical_notified: bool = Field(default=False)
    notified_at: Optional[str] = Field(None, max_length=50)
    notified_to: Optional[str] = Field(None, max_length=200)
    
    # Files
    report_file_url: Optional[str] = Field(None, max_length=500)
    images_urls: Optional[str] = Field(None, description="JSON array")
    dicom_study_id: Optional[str] = Field(None, max_length=100)
    
    # Status
    status: str = Field(default='ordered', max_length=20)
    priority: str = Field(default='routine', max_length=20)
    
    # Quality
    image_quality: Optional[str] = Field(None, max_length=50)
    quality_notes: Optional[str] = None
    
    # Equipment
    equipment_used: Optional[str] = Field(None, max_length=200)
    machine_id: Optional[str] = Field(None, max_length=50)
    radiation_dose: Optional[str] = Field(None, max_length=50)
    
    # Cost
    test_cost: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    
    # Comparison
    comparison_studies: Optional[str] = Field(None, description="JSON array")
    
    # Follow-up
    follow_up_required: bool = Field(default=False)
    follow_up_recommendations: Optional[str] = None
    follow_up_date: Optional[str] = Field(None, max_length=20)
    
    # Verification
    verified_by: Optional[str] = Field(None, max_length=200)
    verified_at: Optional[str] = Field(None, max_length=50)
    
    # Notes
    technician_notes: Optional[str] = None
    radiologist_notes: Optional[str] = None
    notes: Optional[str] = None
    
    rejection_reason: Optional[str] = None
    
    @validator('category')
    def validate_category(cls, v):
        valid = ['diagnostic', 'therapeutic', 'interventional', 'screening']
        if v.lower() not in valid:
            raise ValueError(f"Category must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validator('report_status')
    def validate_report_status(cls, v):
        valid = ['pending', 'preliminary', 'final', 'addendum', 'amended']
        if v.lower() not in valid:
            raise ValueError(f"Report status must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validator('status')
    def validate_status(cls, v):
        valid = ['ordered', 'scheduled', 'in_progress', 'completed', 'cancelled', 'rejected']
        if v.lower() not in valid:
            raise ValueError(f"Status must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validator('priority')
    def validate_priority(cls, v):
        valid = ['routine', 'urgent', 'stat']
        if v.lower() not in valid:
            raise ValueError(f"Priority must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validator('result_type')
    def validate_result_type(cls, v):
        if v:
            valid = ['normal', 'abnormal', 'critical', 'inconclusive']
            if v.lower() not in valid:
                raise ValueError(f"Result type must be one of: {', '.join(valid)}")
            return v.lower()
        return v
    
    @validator('image_quality')
    def validate_image_quality(cls, v):
        if v:
            valid = ['excellent', 'good', 'adequate', 'poor']
            if v.lower() not in valid:
                raise ValueError(f"Image quality must be one of: {', '.join(valid)}")
            return v.lower()
        return v


# Update Schema
class RadiologyUpdate(BaseModel):
    test_name: Optional[str] = Field(None, max_length=200)
    test_code: Optional[str] = Field(None, max_length=50)
    body_part: Optional[str] = Field(None, max_length=100)
    imaging_type: Optional[str] = Field(None, max_length=100)
    category: Optional[str] = Field(None, max_length=100)
    
    scheduled_date: Optional[str] = Field(None, max_length=20)
    scheduled_time: Optional[str] = Field(None, max_length=10)
    
    date_taken: Optional[str] = Field(None, max_length=20)
    time_taken: Optional[str] = Field(None, max_length=10)
    
    clinical_history: Optional[str] = None
    symptoms: Optional[str] = None
    indications: Optional[str] = None
    provisional_diagnosis: Optional[str] = None
    
    contrast_used: Optional[bool] = None
    contrast_type: Optional[str] = Field(None, max_length=100)
    contrast_volume: Optional[str] = Field(None, max_length=50)
    
    preparation_required: Optional[bool] = None
    preparation_instructions: Optional[str] = None
    
    technician_name: Optional[str] = Field(None, max_length=200)
    radiologist_id: Optional[int] = None
    radiologist_name: Optional[str] = Field(None, max_length=200)
    
    report_status: Optional[str] = Field(None, max_length=20)
    findings: Optional[str] = None
    impression: Optional[str] = None
    recommendations: Optional[str] = None
    
    report_date: Optional[str] = Field(None, max_length=20)
    report_time: Optional[str] = Field(None, max_length=10)
    
    result_type: Optional[str] = Field(None, max_length=50)
    
    is_critical: Optional[bool] = None
    critical_findings: Optional[str] = None
    critical_notified: Optional[bool] = None
    notified_at: Optional[str] = Field(None, max_length=50)
    notified_to: Optional[str] = Field(None, max_length=200)
    
    report_file_url: Optional[str] = Field(None, max_length=500)
    images_urls: Optional[str] = None
    dicom_study_id: Optional[str] = Field(None, max_length=100)
    
    status: Optional[str] = Field(None, max_length=20)
    priority: Optional[str] = Field(None, max_length=20)
    
    image_quality: Optional[str] = Field(None, max_length=50)
    quality_notes: Optional[str] = None
    
    equipment_used: Optional[str] = Field(None, max_length=200)
    machine_id: Optional[str] = Field(None, max_length=50)
    radiation_dose: Optional[str] = Field(None, max_length=50)
    
    test_cost: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    
    comparison_studies: Optional[str] = None
    
    follow_up_required: Optional[bool] = None
    follow_up_recommendations: Optional[str] = None
    follow_up_date: Optional[str] = Field(None, max_length=20)
    
    verified_by: Optional[str] = Field(None, max_length=200)
    verified_at: Optional[str] = Field(None, max_length=50)
    
    technician_notes: Optional[str] = None
    radiologist_notes: Optional[str] = None
    notes: Optional[str] = None
    
    rejection_reason: Optional[str] = None


# Response Schema
class RadiologyResponse(RadiologyBase):
    id: int
    test_code: Optional[str]
    category: str
    
    order_date: str
    order_time: str
    
    appointment_id: Optional[int]
    scheduled_date: Optional[str]
    scheduled_time: Optional[str]
    
    date_taken: Optional[str]
    time_taken: Optional[str]
    
    clinical_history: Optional[str]
    symptoms: Optional[str]
    indications: Optional[str]
    provisional_diagnosis: Optional[str]
    
    contrast_used: bool
    contrast_type: Optional[str]
    contrast_volume: Optional[str]
    
    preparation_required: bool
    preparation_instructions: Optional[str]
    
    technician_name: Optional[str]
    radiologist_id: Optional[int]
    radiologist_name: Optional[str]
    
    report_status: str
    findings: Optional[str]
    impression: Optional[str]
    recommendations: Optional[str]
    
    report_date: Optional[str]
    report_time: Optional[str]
    
    result_type: Optional[str]
    
    is_critical: bool
    critical_findings: Optional[str]
    critical_notified: bool
    notified_at: Optional[str]
    notified_to: Optional[str]
    
    report_file_url: Optional[str]
    images_urls: Optional[str]
    dicom_study_id: Optional[str]
    
    status: str
    priority: str
    
    image_quality: Optional[str]
    quality_notes: Optional[str]
    
    equipment_used: Optional[str]
    machine_id: Optional[str]
    radiation_dose: Optional[str]
    
    test_cost: Optional[Decimal]
    
    comparison_studies: Optional[str]
    
    follow_up_required: bool
    follow_up_recommendations: Optional[str]
    follow_up_date: Optional[str]
    
    verified_by: Optional[str]
    verified_at: Optional[str]
    
    technician_notes: Optional[str]
    radiologist_notes: Optional[str]
    notes: Optional[str]
    
    rejection_reason: Optional[str]
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v)
        }


# List Response
class RadiologyListResponse(BaseModel):
    total: int
    items: list[RadiologyResponse]
    page: int
    page_size: int
    total_pages: int


# Schedule Imaging Schema
class RadiologyScheduleSchema(BaseModel):
    scheduled_date: str = Field(..., max_length=20)
    scheduled_time: str = Field(..., max_length=10)
    technician_name: Optional[str] = Field(None, max_length=200)
    equipment_used: Optional[str] = Field(None, max_length=200)
    machine_id: Optional[str] = Field(None, max_length=50)
    preparation_instructions: Optional[str] = None


# Complete Imaging Schema
class RadiologyCompleteImagingSchema(BaseModel):
    date_taken: str = Field(..., max_length=20)
    time_taken: str = Field(..., max_length=10)
    technician_name: str = Field(..., max_length=200)
    images_urls: str = Field(..., description="JSON array of image URLs")
    dicom_study_id: Optional[str] = Field(None, max_length=100)
    image_quality: str = Field(..., max_length=50)
    contrast_used: bool = Field(...)
    contrast_type: Optional[str] = Field(None, max_length=100)
    contrast_volume: Optional[str] = Field(None, max_length=50)
    radiation_dose: Optional[str] = Field(None, max_length=50)
    technician_notes: Optional[str] = None


# Add Report Schema
class RadiologyAddReportSchema(BaseModel):
    radiologist_id: int = Field(..., gt=0)
    radiologist_name: str = Field(..., max_length=200)
    report_date: str = Field(..., max_length=20)
    report_time: str = Field(..., max_length=10)
    
    findings: str = Field(..., description="Radiologist findings")
    impression: str = Field(..., description="Radiologist impression")
    recommendations: Optional[str] = None
    
    result_type: str = Field(..., max_length=50)
    report_status: str = Field(default='final', max_length=20)
    
    is_critical: bool = Field(default=False)
    critical_findings: Optional[str] = None
    
    comparison_studies: Optional[str] = Field(None, description="JSON array")
    follow_up_required: bool = Field(default=False)
    follow_up_recommendations: Optional[str] = None
    follow_up_date: Optional[str] = Field(None, max_length=20)
    
    report_file_url: Optional[str] = Field(None, max_length=500)
    radiologist_notes: Optional[str] = None


# Verify Report Schema
class RadiologyVerifyReportSchema(BaseModel):
    verified_by: str = Field(..., max_length=200)
    verified_at: str = Field(..., max_length=50)
    notes: Optional[str] = None


# Notify Critical Schema
class RadiologyNotifyCriticalSchema(BaseModel):
    notified_to: str = Field(..., max_length=200, description="Person notified")
    notified_at: str = Field(..., max_length=50)
    notification_method: Optional[str] = Field(None, max_length=50, description="phone, email, in_person")
    notes: Optional[str] = None


# Reject Test Schema
class RadiologyRejectSchema(BaseModel):
    rejection_reason: str = Field(..., description="Reason for rejection")
    rejected_by: str = Field(..., max_length=200)


# Comparison Study Schema
class RadiologyComparisonStudySchema(BaseModel):
    study_id: int = Field(..., gt=0, description="Previous radiology study ID")
    study_date: str = Field(..., max_length=20)
    findings: str = Field(..., description="Previous findings")
    notes: Optional[str] = None