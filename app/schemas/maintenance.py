"""
Maintenance Schemas
"""

from pydantic import BaseModel, Field, validator, condecimal
from typing import Optional
from datetime import datetime
from decimal import Decimal


# Base Schema
class MaintenanceBase(BaseModel):
    maintenance_number: str = Field(..., max_length=20, description="Unique maintenance number")
    equipment_id: int = Field(..., gt=0)
    maintenance_type: str = Field(..., max_length=50)
    
    @validator('maintenance_type')
    def validate_maintenance_type(cls, v):
        valid = ['preventive', 'corrective', 'emergency', 'calibration', 'inspection', 'upgrade']
        if v.lower() not in valid:
            raise ValueError(f"Maintenance type must be one of: {', '.join(valid)}")
        return v.lower()


# Create Schema
class MaintenanceCreate(MaintenanceBase):
    maintenance_date: str = Field(..., max_length=20)
    maintenance_time: Optional[str] = Field(None, max_length=10)
    completion_date: Optional[str] = Field(None, max_length=20)
    completion_time: Optional[str] = Field(None, max_length=10)
    next_maintenance_date: Optional[str] = Field(None, max_length=20)
    
    problem_reported: Optional[str] = None
    action_taken: Optional[str] = None
    parts_replaced: Optional[str] = None
    
    technician_name: Optional[str] = Field(None, max_length=200)
    technician_contact: Optional[str] = Field(None, max_length=20)
    
    vendor_name: Optional[str] = Field(None, max_length=200)
    vendor_contact: Optional[str] = Field(None, max_length=20)
    vendor_invoice_number: Optional[str] = Field(None, max_length=50)
    
    cost: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    parts_cost: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    labor_cost: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    
    status: str = Field(default='pending', max_length=20)
    priority: str = Field(default='routine', max_length=20)
    
    downtime_hours: Optional[condecimal(max_digits=5, decimal_places=2, ge=0)] = None
    
    quality_check_done: bool = Field(default=False)
    quality_check_by: Optional[str] = Field(None, max_length=200)
    
    report_file_url: Optional[str] = Field(None, max_length=500)
    invoice_file_url: Optional[str] = Field(None, max_length=500)
    images_urls: Optional[str] = Field(None, description="JSON array")
    
    notes: Optional[str] = None
    recommendations: Optional[str] = None
    
    under_warranty: bool = Field(default=False)
    warranty_claim_number: Optional[str] = Field(None, max_length=50)
    
    @validator('status')
    def validate_status(cls, v):
        valid = ['pending', 'in_progress', 'completed', 'cancelled']
        if v.lower() not in valid:
            raise ValueError(f"Status must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validator('priority')
    def validate_priority(cls, v):
        valid = ['routine', 'urgent', 'emergency']
        if v.lower() not in valid:
            raise ValueError(f"Priority must be one of: {', '.join(valid)}")
        return v.lower()


# Update Schema
class MaintenanceUpdate(BaseModel):
    maintenance_type: Optional[str] = Field(None, max_length=50)
    maintenance_date: Optional[str] = Field(None, max_length=20)
    maintenance_time: Optional[str] = Field(None, max_length=10)
    completion_date: Optional[str] = Field(None, max_length=20)
    completion_time: Optional[str] = Field(None, max_length=10)
    next_maintenance_date: Optional[str] = Field(None, max_length=20)
    
    problem_reported: Optional[str] = None
    action_taken: Optional[str] = None
    parts_replaced: Optional[str] = None
    
    technician_name: Optional[str] = Field(None, max_length=200)
    technician_contact: Optional[str] = Field(None, max_length=20)
    
    vendor_name: Optional[str] = Field(None, max_length=200)
    vendor_contact: Optional[str] = Field(None, max_length=20)
    vendor_invoice_number: Optional[str] = Field(None, max_length=50)
    
    cost: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    parts_cost: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    labor_cost: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    
    status: Optional[str] = Field(None, max_length=20)
    priority: Optional[str] = Field(None, max_length=20)
    
    downtime_hours: Optional[condecimal(max_digits=5, decimal_places=2, ge=0)] = None
    
    quality_check_done: Optional[bool] = None
    quality_check_by: Optional[str] = Field(None, max_length=200)
    
    report_file_url: Optional[str] = Field(None, max_length=500)
    invoice_file_url: Optional[str] = Field(None, max_length=500)
    images_urls: Optional[str] = None
    
    notes: Optional[str] = None
    recommendations: Optional[str] = None
    
    under_warranty: Optional[bool] = None
    warranty_claim_number: Optional[str] = Field(None, max_length=50)


# Response Schema
class MaintenanceResponse(MaintenanceBase):
    id: int
    maintenance_date: str
    maintenance_time: Optional[str]
    completion_date: Optional[str]
    completion_time: Optional[str]
    next_maintenance_date: Optional[str]
    
    problem_reported: Optional[str]
    action_taken: Optional[str]
    parts_replaced: Optional[str]
    
    technician_name: Optional[str]
    technician_contact: Optional[str]
    
    vendor_name: Optional[str]
    vendor_contact: Optional[str]
    vendor_invoice_number: Optional[str]
    
    cost: Optional[Decimal]
    parts_cost: Optional[Decimal]
    labor_cost: Optional[Decimal]
    
    status: str
    priority: str
    
    downtime_hours: Optional[Decimal]
    
    quality_check_done: bool
    quality_check_by: Optional[str]
    
    report_file_url: Optional[str]
    invoice_file_url: Optional[str]
    images_urls: Optional[str]
    
    notes: Optional[str]
    recommendations: Optional[str]
    
    under_warranty: bool
    warranty_claim_number: Optional[str]
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v)
        }


# List Response
class MaintenanceListResponse(BaseModel):
    total: int
    items: list[MaintenanceResponse]
    page: int
    page_size: int
    total_pages: int


# Complete Maintenance Schema
class MaintenanceCompleteSchema(BaseModel):
    completion_date: str = Field(..., max_length=20)
    completion_time: str = Field(..., max_length=10)
    action_taken: str = Field(..., description="Action taken during maintenance")
    quality_check_done: bool = Field(default=True)
    quality_check_by: str = Field(..., max_length=200)
    next_maintenance_date: Optional[str] = Field(None, max_length=20)
    recommendations: Optional[str] = None