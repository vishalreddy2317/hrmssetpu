"""
Test Result Schemas
"""

from pydantic import BaseModel, Field, validator, condecimal
from typing import Optional
from datetime import datetime
from decimal import Decimal


# Base Schema
class TestResultBase(BaseModel):
    result_number: str = Field(..., max_length=20, description="Unique result number")
    patient_id: int = Field(..., gt=0)
    test_name: str = Field(..., max_length=200)
    parameter_name: str = Field(..., max_length=200)
    result_value: str = Field(..., max_length=200)


# Create Schema
class TestResultCreate(TestResultBase):
    lab_test_id: Optional[int] = None
    doctor_id: Optional[int] = None
    
    test_code: Optional[str] = Field(None, max_length=50)
    parameter_code: Optional[str] = Field(None, max_length=50)
    
    result_value_numeric: Optional[condecimal(max_digits=15, decimal_places=4)] = None
    result_unit: Optional[str] = Field(None, max_length=50)
    
    # Normal Range
    normal_range_min: Optional[condecimal(max_digits=15, decimal_places=4)] = None
    normal_range_max: Optional[condecimal(max_digits=15, decimal_places=4)] = None
    normal_range_text: Optional[str] = Field(None, max_length=200)
    reference_range: Optional[str] = Field(None, max_length=200)
    
    # Status
    result_status: str = Field(default='normal', max_length=20)
    
    # Flags
    is_abnormal: bool = Field(default=False)
    is_critical: bool = Field(default=False)
    is_panic_value: bool = Field(default=False)
    
    # Interpretation
    interpretation: Optional[str] = None
    clinical_significance: Optional[str] = None
    
    # Sample Details
    sample_type: Optional[str] = Field(None, max_length=50)
    sample_id: Optional[str] = Field(None, max_length=50)
    sample_collected_date: Optional[str] = Field(None, max_length=20)
    sample_collected_time: Optional[str] = Field(None, max_length=10)
    
    # Testing Details
    test_date: str = Field(..., max_length=20)
    test_time: str = Field(..., max_length=10)
    
    tested_by: Optional[str] = Field(None, max_length=200)
    technician_id: Optional[int] = None
    
    # Verification
    verified_by: Optional[str] = Field(None, max_length=200)
    verified_at: Optional[str] = Field(None, max_length=50)
    
    approved_by: Optional[str] = Field(None, max_length=200)
    approved_at: Optional[str] = Field(None, max_length=50)
    
    # Method and Equipment
    test_method: Optional[str] = Field(None, max_length=200)
    equipment_used: Optional[str] = Field(None, max_length=200)
    
    # Quality Control
    quality_check_passed: bool = Field(default=True)
    quality_check_notes: Optional[str] = None
    
    # Comments
    technician_comments: Optional[str] = None
    doctor_comments: Optional[str] = None
    notes: Optional[str] = None
    
    # Delta Check
    previous_result_value: Optional[str] = Field(None, max_length=200)
    delta_value: Optional[condecimal(max_digits=15, decimal_places=4)] = None
    delta_percentage: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    
    @validator('result_status')
    def validate_result_status(cls, v):
        valid = ['normal', 'abnormal', 'high', 'low', 'critical', 'borderline']
        if v.lower() not in valid:
            raise ValueError(f"Result status must be one of: {', '.join(valid)}")
        return v.lower()


# Update Schema
class TestResultUpdate(BaseModel):
    result_value: Optional[str] = Field(None, max_length=200)
    result_value_numeric: Optional[condecimal(max_digits=15, decimal_places=4)] = None
    result_unit: Optional[str] = Field(None, max_length=50)
    
    result_status: Optional[str] = Field(None, max_length=20)
    
    is_abnormal: Optional[bool] = None
    is_critical: Optional[bool] = None
    is_panic_value: Optional[bool] = None
    
    interpretation: Optional[str] = None
    clinical_significance: Optional[str] = None
    
    verified_by: Optional[str] = Field(None, max_length=200)
    verified_at: Optional[str] = Field(None, max_length=50)
    
    approved_by: Optional[str] = Field(None, max_length=200)
    approved_at: Optional[str] = Field(None, max_length=50)
    
    quality_check_passed: Optional[bool] = None
    quality_check_notes: Optional[str] = None
    
    technician_comments: Optional[str] = None
    doctor_comments: Optional[str] = None
    notes: Optional[str] = None


# Response Schema
class TestResultResponse(TestResultBase):
    id: int
    lab_test_id: Optional[int]
    doctor_id: Optional[int]
    
    test_code: Optional[str]
    parameter_code: Optional[str]
    
    result_value_numeric: Optional[Decimal]
    result_unit: Optional[str]
    
    normal_range_min: Optional[Decimal]
    normal_range_max: Optional[Decimal]
    normal_range_text: Optional[str]
    reference_range: Optional[str]
    
    result_status: str
    
    is_abnormal: bool
    is_critical: bool
    is_panic_value: bool
    
    interpretation: Optional[str]
    clinical_significance: Optional[str]
    
    sample_type: Optional[str]
    sample_id: Optional[str]
    sample_collected_date: Optional[str]
    sample_collected_time: Optional[str]
    
    test_date: str
    test_time: str
    
    tested_by: Optional[str]
    technician_id: Optional[int]
    
    verified_by: Optional[str]
    verified_at: Optional[str]
    
    approved_by: Optional[str]
    approved_at: Optional[str]
    
    test_method: Optional[str]
    equipment_used: Optional[str]
    
    quality_check_passed: bool
    quality_check_notes: Optional[str]
    
    technician_comments: Optional[str]
    doctor_comments: Optional[str]
    notes: Optional[str]
    
    previous_result_value: Optional[str]
    delta_value: Optional[Decimal]
    delta_percentage: Optional[Decimal]
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v)
        }


# List Response
class TestResultListResponse(BaseModel):
    total: int
    items: list[TestResultResponse]
    page: int
    page_size: int
    total_pages: int


# Test Result Filter Schema
class TestResultFilterSchema(BaseModel):
    patient_id: Optional[int] = None
    lab_test_id: Optional[int] = None
    doctor_id: Optional[int] = None
    
    test_name: Optional[str] = Field(None, max_length=200)
    parameter_name: Optional[str] = Field(None, max_length=200)
    
    result_status: Optional[str] = Field(None, max_length=20)
    is_critical: Optional[bool] = None
    is_abnormal: Optional[bool] = None
    
    start_date: Optional[str] = Field(None, max_length=20)
    end_date: Optional[str] = Field(None, max_length=20)
    
    sample_type: Optional[str] = Field(None, max_length=50)


# Bulk Test Results Create
class BulkTestResultsCreate(BaseModel):
    lab_test_id: int = Field(..., gt=0)
    patient_id: int = Field(..., gt=0)
    doctor_id: Optional[int] = None
    
    test_date: str = Field(..., max_length=20)
    test_time: str = Field(..., max_length=10)
    
    results: list[dict] = Field(..., min_items=1, description="List of parameter results")
    
    tested_by: str = Field(..., max_length=200)
    technician_id: Optional[int] = None


# Critical Values Alert Schema
class CriticalValuesAlertSchema(BaseModel):
    result_id: int
    patient_id: int
    patient_name: str
    
    test_name: str
    parameter_name: str
    result_value: str
    normal_range: str
    
    is_critical: bool
    is_panic_value: bool
    
    doctor_id: Optional[int]
    doctor_name: Optional[str]
    
    alert_time: str
    notified_to: Optional[str]