"""
Staff Schemas
"""

from pydantic import BaseModel, Field, validator, EmailStr, condecimal
from typing import Optional
from datetime import datetime
from decimal import Decimal
import re


# Base Schema
class StaffBase(BaseModel):
    staff_id: str = Field(..., max_length=20, description="Unique staff ID")
    first_name: str = Field(..., max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    last_name: str = Field(..., max_length=100)
    
    email: EmailStr = Field(..., description="Email address")
    phone: str = Field(..., max_length=20)
    
    @validator('phone')
    def validate_phone(cls, v):
        if v and not re.match(r'^\+?1?\d{9,15}$', v.replace('-', '').replace(' ', '')):
            raise ValueError("Invalid phone number format")
        return v


# Create Schema
class StaffCreate(StaffBase):
    user_id: Optional[int] = None
    
    alternate_phone: Optional[str] = Field(None, max_length=20)
    
    # Address
    address: str = Field(...)
    city: str = Field(..., max_length=100)
    state: str = Field(..., max_length=100)
    country: str = Field(default="USA", max_length=100)
    pincode: str = Field(..., max_length=20)
    
    # Employment Details
    employee_id: str = Field(..., max_length=50)
    designation: str = Field(..., max_length=100)
    department: Optional[str] = Field(None, max_length=100)
    role: str = Field(..., max_length=50)
    
    hospital_id: Optional[int] = None
    
    # Work Details
    joining_date: str = Field(..., max_length=20)
    leaving_date: Optional[str] = Field(None, max_length=20)
    shift: Optional[str] = Field(None, max_length=20)
    
    # Salary
    salary: Optional[condecimal(max_digits=12, decimal_places=2, gt=0)] = None
    salary_currency: str = Field(default="USD", max_length=3)
    
    # Qualifications
    qualification: str = Field(..., max_length=200)
    experience_years: int = Field(default=0, ge=0)
    
    # Availability
    is_available: bool = Field(default=True)
    is_on_duty: bool = Field(default=False)
    status: str = Field(default='active', max_length=20)
    
    # Emergency Contact
    emergency_contact_name: Optional[str] = Field(None, max_length=200)
    emergency_contact_phone: Optional[str] = Field(None, max_length=20)
    emergency_contact_relation: Optional[str] = Field(None, max_length=50)
    
    # Identification
    national_id: Optional[str] = Field(None, max_length=50)
    
    # Additional
    skills: Optional[str] = None
    certifications: Optional[str] = None
    languages_spoken: Optional[str] = Field(None, max_length=200)
    notes: Optional[str] = None
    profile_image: Optional[str] = Field(None, max_length=500)
    
    @validator('role')
    def validate_role(cls, v):
        valid = [
            'receptionist', 'accountant', 'hr', 'admin', 'security',
            'housekeeping', 'lab_technician', 'pharmacist', 'it_support',
            'maintenance', 'dietitian', 'social_worker'
        ]
        if v.lower() not in valid:
            raise ValueError(f"Role must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validator('status')
    def validate_status(cls, v):
        valid = ['active', 'on_leave', 'resigned', 'terminated', 'retired', 'suspended']
        if v.lower() not in valid:
            raise ValueError(f"Status must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validator('shift')
    def validate_shift(cls, v):
        if v:
            valid = ['morning', 'evening', 'night', 'rotating', 'general']
            if v.lower() not in valid:
                raise ValueError(f"Shift must be one of: {', '.join(valid)}")
            return v.lower()
        return v


# Update Schema
class StaffUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    alternate_phone: Optional[str] = Field(None, max_length=20)
    
    address: Optional[str] = None
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    pincode: Optional[str] = Field(None, max_length=20)
    
    designation: Optional[str] = Field(None, max_length=100)
    department: Optional[str] = Field(None, max_length=100)
    role: Optional[str] = Field(None, max_length=50)
    
    hospital_id: Optional[int] = None
    
    leaving_date: Optional[str] = Field(None, max_length=20)
    shift: Optional[str] = Field(None, max_length=20)
    
    salary: Optional[condecimal(max_digits=12, decimal_places=2, gt=0)] = None
    salary_currency: Optional[str] = Field(None, max_length=3)
    
    qualification: Optional[str] = Field(None, max_length=200)
    experience_years: Optional[int] = Field(None, ge=0)
    
    is_available: Optional[bool] = None
    is_on_duty: Optional[bool] = None
    status: Optional[str] = Field(None, max_length=20)
    
    emergency_contact_name: Optional[str] = Field(None, max_length=200)
    emergency_contact_phone: Optional[str] = Field(None, max_length=20)
    emergency_contact_relation: Optional[str] = Field(None, max_length=50)
    
    national_id: Optional[str] = Field(None, max_length=50)
    
    skills: Optional[str] = None
    certifications: Optional[str] = None
    languages_spoken: Optional[str] = Field(None, max_length=200)
    notes: Optional[str] = None
    profile_image: Optional[str] = Field(None, max_length=500)


# Response Schema
class StaffResponse(StaffBase):
    id: int
    user_id: Optional[int]
    
    alternate_phone: Optional[str]
    
    address: str
    city: str
    state: str
    country: str
    pincode: str
    
    employee_id: str
    designation: str
    department: Optional[str]
    role: str
    
    hospital_id: Optional[int]
    
    joining_date: str
    leaving_date: Optional[str]
    shift: Optional[str]
    
    salary: Optional[Decimal]
    salary_currency: str
    
    qualification: str
    experience_years: int
    
    is_available: bool
    is_on_duty: bool
    status: str
    
    emergency_contact_name: Optional[str]
    emergency_contact_phone: Optional[str]
    emergency_contact_relation: Optional[str]
    
    national_id: Optional[str]
    
    skills: Optional[str]
    certifications: Optional[str]
    languages_spoken: Optional[str]
    notes: Optional[str]
    profile_image: Optional[str]
    
    full_name: str
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v)
        }


# List Response
class StaffListResponse(BaseModel):
    total: int
    items: list[StaffResponse]
    page: int
    page_size: int
    total_pages: int


# Staff Filter Schema
class StaffFilterSchema(BaseModel):
    role: Optional[str] = Field(None, max_length=50)
    department: Optional[str] = Field(None, max_length=100)
    designation: Optional[str] = Field(None, max_length=100)
    hospital_id: Optional[int] = None
    
    status: Optional[str] = Field(None, max_length=20)
    is_available: Optional[bool] = None
    is_on_duty: Optional[bool] = None
    
    shift: Optional[str] = Field(None, max_length=20)
    
    min_experience: Optional[int] = Field(None, ge=0)
    max_experience: Optional[int] = Field(None, ge=0)
    
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)


# Staff Summary Schema
class StaffSummarySchema(BaseModel):
    total_staff: int
    active_staff: int
    on_leave_staff: int
    on_duty_staff: int
    
    by_role: dict  # {role: count}
    by_department: dict  # {department: count}
    by_shift: dict  # {shift: count}
    
    average_experience_years: float
    total_salary_expense: Decimal
    
    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }


# Duty Status Update
class StaffDutyStatusUpdate(BaseModel):
    is_on_duty: bool = Field(...)
    shift: Optional[str] = Field(None, max_length=20)
    updated_by: str = Field(..., max_length=200)
    notes: Optional[str] = None


# Availability Update
class StaffAvailabilityUpdate(BaseModel):
    is_available: bool = Field(...)
    reason: Optional[str] = None
    unavailable_from: Optional[str] = Field(None, max_length=20)
    unavailable_to: Optional[str] = Field(None, max_length=20)
    updated_by: str = Field(..., max_length=200)


# Staff Assignment Schema
class StaffAssignmentSchema(BaseModel):
    staff_id: int = Field(..., gt=0)
    assignment_type: str = Field(..., max_length=50, description="department, shift, task, special_duty")
    
    department_id: Optional[int] = None
    shift_id: Optional[int] = None
    
    start_date: str = Field(..., max_length=20)
    end_date: Optional[str] = Field(None, max_length=20)
    
    assigned_by: str = Field(..., max_length=200)
    notes: Optional[str] = None


# Staff Performance Schema
class StaffPerformanceSchema(BaseModel):
    staff_id: int
    staff_name: str
    role: str
    department: Optional[str]
    
    review_period_start: str
    review_period_end: str
    
    attendance_percentage: float
    punctuality_score: float
    task_completion_rate: float
    customer_satisfaction_score: Optional[float]
    
    total_leaves_taken: int
    total_absences: int
    total_working_days: int
    
    strengths: Optional[str]
    areas_for_improvement: Optional[str]
    
    overall_rating: float  # 1-5
    reviewed_by: str
    review_date: str


# Bulk Staff Create Schema
class BulkStaffCreateSchema(BaseModel):
    staff_data: list[StaffCreate] = Field(..., min_items=1)
    created_by: str = Field(..., max_length=200)


# Staff Transfer Schema
class StaffTransferSchema(BaseModel):
    staff_id: int = Field(..., gt=0)
    
    from_department: str = Field(..., max_length=100)
    to_department: str = Field(..., max_length=100)
    
    from_hospital_id: Optional[int] = None
    to_hospital_id: Optional[int] = None
    
    transfer_date: str = Field(..., max_length=20)
    transfer_reason: str = Field(...)
    
    new_designation: Optional[str] = Field(None, max_length=100)
    new_salary: Optional[condecimal(max_digits=12, decimal_places=2, gt=0)] = None
    
    approved_by: str = Field(..., max_length=200)
    notes: Optional[str] = None


# Staff Resignation Schema
class StaffResignationSchema(BaseModel):
    staff_id: int = Field(..., gt=0)
    
    resignation_date: str = Field(..., max_length=20)
    leaving_date: str = Field(..., max_length=20)
    notice_period_days: int = Field(..., ge=0)
    
    reason: str = Field(...)
    feedback: Optional[str] = None
    
    exit_interview_done: bool = Field(default=False)
    exit_interview_notes: Optional[str] = None
    
    final_settlement_amount: Optional[condecimal(max_digits=12, decimal_places=2)] = None
    
    processed_by: str = Field(..., max_length=200)


# Staff Attendance Summary
class StaffAttendanceSummarySchema(BaseModel):
    staff_id: int
    staff_name: str
    
    month: int
    year: int
    
    total_working_days: int
    present_days: int
    absent_days: int
    leave_days: int
    half_days: int
    
    late_arrivals: int
    early_departures: int
    
    total_hours_worked: float
    overtime_hours: float
    
    attendance_percentage: float


# Staff Salary Update Schema
class StaffSalaryUpdateSchema(BaseModel):
    new_salary: condecimal(max_digits=12, decimal_places=2, gt=0) = Field(...)
    effective_date: str = Field(..., max_length=20)
    
    increment_type: str = Field(..., max_length=50, description="annual, promotion, performance, market_adjustment")
    increment_percentage: Optional[float] = Field(None, ge=0)
    
    reason: str = Field(...)
    approved_by: str = Field(..., max_length=200)
    notes: Optional[str] = None


# Staff Document Schema
class StaffDocumentSchema(BaseModel):
    staff_id: int = Field(..., gt=0)
    
    document_type: str = Field(..., max_length=50, description="resume, certificate, id_proof, offer_letter")
    document_name: str = Field(..., max_length=200)
    document_url: str = Field(..., max_length=500)
    
    document_number: Optional[str] = Field(None, max_length=100)
    issue_date: Optional[str] = Field(None, max_length=20)
    expiry_date: Optional[str] = Field(None, max_length=20)
    
    uploaded_by: str = Field(..., max_length=200)
    notes: Optional[str] = None