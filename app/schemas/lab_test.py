"""
Lab Test Schemas
"""

from pydantic import BaseModel, Field, validator, condecimal
from typing import Optional
from datetime import datetime
from decimal import Decimal


# Base Schema
class LabTestBase(BaseModel):
    test_name: str = Field(..., max_length=200, description="Name of the test")
    test_code: Optional[str] = Field(None, max_length=50)
    test_category: str = Field(..., max_length=100)
    test_type: str = Field(..., max_length=100)
    
    @validator('test_category')
    def validate_category(cls, v):
        valid = ['blood', 'urine', 'stool', 'imaging', 'pathology', 
                'microbiology', 'biochemistry', 'hematology', 'serology']
        if v.lower() not in valid:
            raise ValueError(f"Test category must be one of: {', '.join(valid)}")
        return v.lower()


# Create Schema
class LabTestCreate(LabTestBase):
    test_number: str = Field(..., max_length=20, description="Unique test number")
    patient_id: int = Field(..., gt=0)
    ordered_by_doctor_id: int = Field(..., gt=0)
    
    status: str = Field(default='pending', max_length=20)
    order_date: str = Field(..., max_length=20)
    order_time: str = Field(..., max_length=10)
    
    sample_collection_date: Optional[str] = Field(None, max_length=20)
    sample_collection_time: Optional[str] = Field(None, max_length=10)
    report_date: Optional[str] = Field(None, max_length=20)
    report_time: Optional[str] = Field(None, max_length=10)
    
    sample_type: Optional[str] = Field(None, max_length=50)
    sample_id: Optional[str] = Field(None, max_length=50)
    sample_collected_by: Optional[str] = Field(None, max_length=100)
    
    priority: str = Field(default='routine', max_length=20)
    special_instructions: Optional[str] = None
    fasting_required: bool = Field(default=False)
    
    test_cost: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    clinical_notes: Optional[str] = None
    rejection_reason: Optional[str] = None
    
    @validator('status')
    def validate_status(cls, v):
        valid = ['pending', 'sample_collected', 'in_progress', 'completed', 'cancelled', 'rejected']
        if v.lower() not in valid:
            raise ValueError(f"Status must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validator('priority')
    def validate_priority(cls, v):
        valid = ['routine', 'urgent', 'stat']
        if v.lower() not in valid:
            raise ValueError(f"Priority must be one of: {', '.join(valid)}")
        return v.lower()


# Update Schema
class LabTestUpdate(BaseModel):
    test_name: Optional[str] = Field(None, max_length=200)
    test_code: Optional[str] = Field(None, max_length=50)
    test_category: Optional[str] = Field(None, max_length=100)
    test_type: Optional[str] = Field(None, max_length=100)
    status: Optional[str] = Field(None, max_length=20)
    
    sample_collection_date: Optional[str] = Field(None, max_length=20)
    sample_collection_time: Optional[str] = Field(None, max_length=10)
    report_date: Optional[str] = Field(None, max_length=20)
    report_time: Optional[str] = Field(None, max_length=10)
    
    sample_type: Optional[str] = Field(None, max_length=50)
    sample_id: Optional[str] = Field(None, max_length=50)
    sample_collected_by: Optional[str] = Field(None, max_length=100)
    
    priority: Optional[str] = Field(None, max_length=20)
    special_instructions: Optional[str] = None
    fasting_required: Optional[bool] = None
    
    test_cost: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    clinical_notes: Optional[str] = None
    rejection_reason: Optional[str] = None


# Response Schema
class LabTestResponse(LabTestBase):
    id: int
    test_number: str
    patient_id: int
    ordered_by_doctor_id: int
    
    status: str
    order_date: str
    order_time: str
    
    sample_collection_date: Optional[str]
    sample_collection_time: Optional[str]
    report_date: Optional[str]
    report_time: Optional[str]
    
    sample_type: Optional[str]
    sample_id: Optional[str]
    sample_collected_by: Optional[str]
    
    priority: str
    special_instructions: Optional[str]
    fasting_required: bool
    
    test_cost: Optional[Decimal]
    clinical_notes: Optional[str]
    rejection_reason: Optional[str]
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v)
        }


# List Response
class LabTestListResponse(BaseModel):
    total: int
    items: list[LabTestResponse]
    page: int
    page_size: int
    total_pages: int