"""
Leave Schemas
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


# Base Schema
class LeaveBase(BaseModel):
    leave_number: str = Field(..., max_length=20, description="Unique leave number")
    employee_name: str = Field(..., max_length=200)
    employee_id: str = Field(..., max_length=50)
    leave_type: str = Field(..., max_length=50)
    
    @validator('leave_type')
    def validate_leave_type(cls, v):
        valid = ['sick', 'casual', 'earned', 'maternity', 'paternity',
                'unpaid', 'compensatory', 'bereavement', 'study', 'sabbatical']
        if v.lower() not in valid:
            raise ValueError(f"Leave type must be one of: {', '.join(valid)}")
        return v.lower()


# Create Schema
class LeaveCreate(LeaveBase):
    staff_id: Optional[int] = None
    doctor_id: Optional[int] = None
    nurse_id: Optional[int] = None
    
    start_date: str = Field(..., max_length=20)
    end_date: str = Field(..., max_length=20)
    total_days: int = Field(..., gt=0)
    
    is_half_day: bool = Field(default=False)
    half_day_session: Optional[str] = Field(None, max_length=20)
    
    reason: str = Field(..., description="Reason for leave")
    application_date: str = Field(..., max_length=20)
    
    status: str = Field(default='pending', max_length=20)
    
    approved_by: Optional[str] = Field(None, max_length=200)
    approval_date: Optional[str] = Field(None, max_length=20)
    approval_remarks: Optional[str] = None
    
    rejected_by: Optional[str] = Field(None, max_length=200)
    rejection_date: Optional[str] = Field(None, max_length=20)
    rejection_reason: Optional[str] = None
    
    attachment_url: Optional[str] = Field(None, max_length=500)
    medical_certificate_url: Optional[str] = Field(None, max_length=500)
    
    contact_number: Optional[str] = Field(None, max_length=20)
    emergency_contact: Optional[str] = Field(None, max_length=20)
    
    handover_to: Optional[str] = Field(None, max_length=200)
    handover_notes: Optional[str] = None
    notes: Optional[str] = None
    
    @validator('status')
    def validate_status(cls, v):
        valid = ['pending', 'approved', 'rejected', 'cancelled', 'withdrawn']
        if v.lower() not in valid:
            raise ValueError(f"Status must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validator('half_day_session')
    def validate_half_day_session(cls, v, values):
        if values.get('is_half_day') and v not in ['first_half', 'second_half', None]:
            raise ValueError("Half day session must be 'first_half' or 'second_half'")
        return v


# Update Schema
class LeaveUpdate(BaseModel):
    start_date: Optional[str] = Field(None, max_length=20)
    end_date: Optional[str] = Field(None, max_length=20)
    total_days: Optional[int] = Field(None, gt=0)
    
    is_half_day: Optional[bool] = None
    half_day_session: Optional[str] = Field(None, max_length=20)
    
    reason: Optional[str] = None
    status: Optional[str] = Field(None, max_length=20)
    
    approved_by: Optional[str] = Field(None, max_length=200)
    approval_date: Optional[str] = Field(None, max_length=20)
    approval_remarks: Optional[str] = None
    
    rejected_by: Optional[str] = Field(None, max_length=200)
    rejection_date: Optional[str] = Field(None, max_length=20)
    rejection_reason: Optional[str] = None
    
    attachment_url: Optional[str] = Field(None, max_length=500)
    medical_certificate_url: Optional[str] = Field(None, max_length=500)
    
    contact_number: Optional[str] = Field(None, max_length=20)
    emergency_contact: Optional[str] = Field(None, max_length=20)
    
    handover_to: Optional[str] = Field(None, max_length=200)
    handover_notes: Optional[str] = None
    notes: Optional[str] = None


# Response Schema
class LeaveResponse(LeaveBase):
    id: int
    staff_id: Optional[int]
    doctor_id: Optional[int]
    nurse_id: Optional[int]
    
    start_date: str
    end_date: str
    total_days: int
    
    is_half_day: bool
    half_day_session: Optional[str]
    
    reason: str
    application_date: str
    status: str
    
    approved_by: Optional[str]
    approval_date: Optional[str]
    approval_remarks: Optional[str]
    
    rejected_by: Optional[str]
    rejection_date: Optional[str]
    rejection_reason: Optional[str]
    
    attachment_url: Optional[str]
    medical_certificate_url: Optional[str]
    
    contact_number: Optional[str]
    emergency_contact: Optional[str]
    
    handover_to: Optional[str]
    handover_notes: Optional[str]
    notes: Optional[str]
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# List Response
class LeaveListResponse(BaseModel):
    total: int
    items: list[LeaveResponse]
    page: int
    page_size: int
    total_pages: int


# Approve/Reject Schema
class LeaveApprovalSchema(BaseModel):
    approved_by: str = Field(..., max_length=200)
    approval_remarks: Optional[str] = None


class LeaveRejectionSchema(BaseModel):
    rejected_by: str = Field(..., max_length=200)
    rejection_reason: str = Field(..., description="Reason for rejection")