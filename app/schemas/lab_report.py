"""
Lab Report Schemas
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


# Base Schema
class LabReportBase(BaseModel):
    report_number: str = Field(..., max_length=20, description="Unique report number")
    lab_test_id: int = Field(..., gt=0)
    patient_id: int = Field(..., gt=0)


# Create Schema
class LabReportCreate(LabReportBase):
    report_date: str = Field(..., max_length=20)
    report_time: str = Field(..., max_length=10)
    
    test_results: str = Field(..., description="JSON format with test parameters")
    interpretation: Optional[str] = None
    findings: Optional[str] = None
    
    result_status: str = Field(default='normal', max_length=20)
    
    tested_by: Optional[str] = Field(None, max_length=200)
    verified_by: Optional[str] = Field(None, max_length=200)
    approved_by_doctor_id: Optional[int] = None
    
    reference_ranges: Optional[str] = Field(None, description="JSON format")
    technician_notes: Optional[str] = None
    doctor_notes: Optional[str] = None
    
    report_file_url: Optional[str] = Field(None, max_length=500)
    images_urls: Optional[str] = Field(None, description="JSON array")
    
    is_critical: bool = Field(default=False)
    critical_value_notified: bool = Field(default=False)
    notified_at: Optional[str] = Field(None, max_length=50)
    
    quality_check_passed: bool = Field(default=True)
    quality_check_notes: Optional[str] = None
    
    @validator('result_status')
    def validate_status(cls, v):
        valid = ['normal', 'abnormal', 'critical', 'inconclusive', 'pending_review']
        if v.lower() not in valid:
            raise ValueError(f"Result status must be one of: {', '.join(valid)}")
        return v.lower()


# Update Schema
class LabReportUpdate(BaseModel):
    test_results: Optional[str] = None
    interpretation: Optional[str] = None
    findings: Optional[str] = None
    
    result_status: Optional[str] = Field(None, max_length=20)
    
    tested_by: Optional[str] = Field(None, max_length=200)
    verified_by: Optional[str] = Field(None, max_length=200)
    approved_by_doctor_id: Optional[int] = None
    
    reference_ranges: Optional[str] = None
    technician_notes: Optional[str] = None
    doctor_notes: Optional[str] = None
    
    report_file_url: Optional[str] = Field(None, max_length=500)
    images_urls: Optional[str] = None
    
    is_critical: Optional[bool] = None
    critical_value_notified: Optional[bool] = None
    notified_at: Optional[str] = Field(None, max_length=50)
    
    quality_check_passed: Optional[bool] = None
    quality_check_notes: Optional[str] = None


# Response Schema
class LabReportResponse(LabReportBase):
    id: int
    report_date: str
    report_time: str
    
    test_results: str
    interpretation: Optional[str]
    findings: Optional[str]
    
    result_status: str
    
    tested_by: Optional[str]
    verified_by: Optional[str]
    approved_by_doctor_id: Optional[int]
    
    reference_ranges: Optional[str]
    technician_notes: Optional[str]
    doctor_notes: Optional[str]
    
    report_file_url: Optional[str]
    images_urls: Optional[str]
    
    is_critical: bool
    critical_value_notified: bool
    notified_at: Optional[str]
    
    quality_check_passed: bool
    quality_check_notes: Optional[str]
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# List Response
class LabReportListResponse(BaseModel):
    total: int
    items: list[LabReportResponse]
    page: int
    page_size: int
    total_pages: int