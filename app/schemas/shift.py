"""
Shift Schemas
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


# Base Schema
class ShiftBase(BaseModel):
    shift_name: str = Field(..., max_length=100, description="Shift name")
    shift_code: str = Field(..., max_length=20, description="Unique shift code")
    start_time: str = Field(..., max_length=10)
    end_time: str = Field(..., max_length=10)
    
    @validator('shift_code')
    def validate_shift_code(cls, v):
        # Code should be uppercase
        if not v.isupper():
            raise ValueError("Shift code must be uppercase")
        return v


# Create Schema
class ShiftCreate(ShiftBase):
    duration_hours: int = Field(..., gt=0, description="Duration in hours")
    break_duration_minutes: int = Field(default=30, ge=0, description="Break duration in minutes")
    
    shift_type: str = Field(..., max_length=20)
    
    applicable_days: Optional[str] = Field(None, max_length=100, description="JSON array")
    
    grace_period_minutes: int = Field(default=15, ge=0)
    
    overtime_applicable: bool = Field(default=True)
    overtime_rate_multiplier: Optional[float] = Field(default=1.5, ge=1.0)
    
    status: str = Field(default='active', max_length=20)
    description: Optional[str] = None
    
    @validator('shift_type')
    def validate_shift_type(cls, v):
        valid = ['morning', 'evening', 'night', 'general', 'rotating', 'split']
        if v.lower() not in valid:
            raise ValueError(f"Shift type must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validator('status')
    def validate_status(cls, v):
        valid = ['active', 'inactive']
        if v.lower() not in valid:
            raise ValueError(f"Status must be one of: {', '.join(valid)}")
        return v.lower()


# Update Schema
class ShiftUpdate(BaseModel):
    shift_name: Optional[str] = Field(None, max_length=100)
    start_time: Optional[str] = Field(None, max_length=10)
    end_time: Optional[str] = Field(None, max_length=10)
    
    duration_hours: Optional[int] = Field(None, gt=0)
    break_duration_minutes: Optional[int] = Field(None, ge=0)
    
    shift_type: Optional[str] = Field(None, max_length=20)
    applicable_days: Optional[str] = Field(None, max_length=100)
    
    grace_period_minutes: Optional[int] = Field(None, ge=0)
    
    overtime_applicable: Optional[bool] = None
    overtime_rate_multiplier: Optional[float] = Field(None, ge=1.0)
    
    status: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = None


# Response Schema
class ShiftResponse(ShiftBase):
    id: int
    
    duration_hours: int
    break_duration_minutes: int
    
    shift_type: str
    applicable_days: Optional[str]
    
    grace_period_minutes: int
    
    overtime_applicable: bool
    overtime_rate_multiplier: Optional[float]
    
    status: str
    description: Optional[str]
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# List Response
class ShiftListResponse(BaseModel):
    total: int
    items: list[ShiftResponse]
    page: int
    page_size: int
    total_pages: int


# Shift with Schedule Count
class ShiftWithScheduleCountResponse(ShiftResponse):
    total_schedules: int
    active_schedules: int
    doctors_assigned: int


# Shift Coverage Analysis
class ShiftCoverageAnalysisSchema(BaseModel):
    shift_id: int
    shift_name: str
    start_time: str
    end_time: str
    
    date: str
    day_of_week: str
    
    required_doctors: int
    scheduled_doctors: int
    available_doctors: int
    
    is_fully_covered: bool
    coverage_percentage: float
    
    departments: dict  # {department_name: doctor_count}


# Shift Statistics
class ShiftStatisticsSchema(BaseModel):
    shift_id: int
    shift_name: str
    
    period_start: str
    period_end: str
    
    total_schedules: int
    total_doctors: int
    total_hours: float
    
    average_doctors_per_day: float
    most_busy_day: Optional[str]
    least_busy_day: Optional[str]


# Shift Template Schema
class ShiftTemplateSchema(BaseModel):
    template_name: str = Field(..., max_length=100)
    description: Optional[str] = None
    
    morning_shift: dict  # {name, start_time, end_time, duration}
    evening_shift: dict
    night_shift: dict
    
    created_by: str = Field(..., max_length=200)


# Apply Shift Template
class ApplyShiftTemplateSchema(BaseModel):
    template_id: int = Field(..., gt=0)
    department_id: Optional[int] = None
    
    effective_date: str = Field(..., max_length=20)
    applied_by: str = Field(..., max_length=200)


# Shift Rotation Schema
class ShiftRotationSchema(BaseModel):
    rotation_name: str = Field(..., max_length=100)
    
    shift_ids: list[int] = Field(..., min_items=2, description="Shifts in rotation order")
    rotation_days: int = Field(..., ge=1, description="Days before rotation")
    
    doctor_ids: list[int] = Field(..., min_items=1)
    department_id: Optional[int] = None
    
    start_date: str = Field(..., max_length=20)
    end_date: Optional[str] = Field(None, max_length=20)
    
    created_by: str = Field(..., max_length=200)


# Shift Swap Schema
class ShiftSwapSchema(BaseModel):
    from_shift_id: int = Field(..., gt=0)
    to_shift_id: int = Field(..., gt=0)
    
    doctor_id: int = Field(..., gt=0)
    date: str = Field(..., max_length=20)
    
    reason: str = Field(..., description="Reason for shift swap")
    requested_by: str = Field(..., max_length=200)


# Shift Assignment Schema
class ShiftAssignmentSchema(BaseModel):
    shift_id: int = Field(..., gt=0)
    doctor_ids: list[int] = Field(..., min_items=1)
    
    start_date: str = Field(..., max_length=20)
    end_date: str = Field(..., max_length=20)
    
    days_of_week: list[int] = Field(..., description="0=Monday, 6=Sunday")
    
    assigned_by: str = Field(..., max_length=200)
    notes: Optional[str] = None


# Shift Conflict Check Schema
class ShiftConflictCheckSchema(BaseModel):
    doctor_id: int = Field(..., gt=0)
    date: str = Field(..., max_length=20)
    shift_id: int = Field(..., gt=0)


# Shift Conflict Response
class ShiftConflictResponse(BaseModel):
    has_conflict: bool
    conflict_type: Optional[str]  # overlapping, double_booking, rest_period_violation
    existing_shift: Optional[ShiftResponse]
    message: str


# Shift Filter Schema
class ShiftFilterSchema(BaseModel):
    shift_type: Optional[str] = Field(None, max_length=20)
    status: Optional[str] = Field(None, max_length=20)
    min_duration: Optional[int] = Field(None, ge=1)
    max_duration: Optional[int] = Field(None, ge=1)


# Working Hours Calculation
class WorkingHoursCalculationSchema(BaseModel):
    shift_id: int
    include_break: bool = Field(default=False)
    
    # For overtime calculation
    actual_start_time: Optional[str] = Field(None, max_length=10)
    actual_end_time: Optional[str] = Field(None, max_length=10)


# Working Hours Response
class WorkingHoursResponse(BaseModel):
    shift_id: int
    shift_name: str
    
    scheduled_hours: float
    actual_hours: Optional[float]
    
    regular_hours: float
    overtime_hours: float
    
    break_duration_hours: float
    net_working_hours: float
    
    overtime_pay_multiplier: float