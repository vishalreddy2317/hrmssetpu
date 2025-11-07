"""
Schedule Schemas
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


# Base Schema
class ScheduleBase(BaseModel):
    schedule_date: str = Field(..., max_length=20, description="Schedule date")
    shift_id: int = Field(..., gt=0)


# Create Schema
class ScheduleCreate(ScheduleBase):
    doctor_id: Optional[int] = None
    department_id: Optional[int] = None
    
    # Timing (can override shift timings)
    start_time: Optional[str] = Field(None, max_length=10)
    end_time: Optional[str] = Field(None, max_length=10)
    
    # Availability
    is_available: bool = Field(default=True)
    max_appointments: Optional[int] = Field(None, ge=0)
    
    # Status
    status: str = Field(default='scheduled', max_length=20)
    day_type: str = Field(default='working', max_length=20)
    
    # On-Call
    is_on_call: bool = Field(default=False)
    
    # Notes
    notes: Optional[str] = None
    
    @validator('status')
    def validate_status(cls, v):
        valid = ['scheduled', 'completed', 'cancelled', 'on_leave', 'rescheduled']
        if v.lower() not in valid:
            raise ValueError(f"Status must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validator('day_type')
    def validate_day_type(cls, v):
        valid = ['working', 'holiday', 'weekend', 'on_call', 'emergency']
        if v.lower() not in valid:
            raise ValueError(f"Day type must be one of: {', '.join(valid)}")
        return v.lower()


# Update Schema
class ScheduleUpdate(BaseModel):
    schedule_date: Optional[str] = Field(None, max_length=20)
    doctor_id: Optional[int] = None
    shift_id: Optional[int] = Field(None, gt=0)
    department_id: Optional[int] = None
    
    start_time: Optional[str] = Field(None, max_length=10)
    end_time: Optional[str] = Field(None, max_length=10)
    
    is_available: Optional[bool] = None
    max_appointments: Optional[int] = Field(None, ge=0)
    
    status: Optional[str] = Field(None, max_length=20)
    day_type: Optional[str] = Field(None, max_length=20)
    
    is_on_call: Optional[bool] = None
    notes: Optional[str] = None


# Response Schema
class ScheduleResponse(ScheduleBase):
    id: int
    doctor_id: Optional[int]
    department_id: Optional[int]
    
    start_time: Optional[str]
    end_time: Optional[str]
    
    is_available: bool
    max_appointments: Optional[int]
    
    status: str
    day_type: str
    
    is_on_call: bool
    notes: Optional[str]
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# List Response
class ScheduleListResponse(BaseModel):
    total: int
    items: list[ScheduleResponse]
    page: int
    page_size: int
    total_pages: int


# Schedule with Details Response
class ScheduleDetailedResponse(ScheduleResponse):
    doctor_name: Optional[str]
    shift_name: str
    shift_start_time: str
    shift_end_time: str
    department_name: Optional[str]


# Weekly Schedule Response
class WeeklyScheduleResponse(BaseModel):
    week_start_date: str
    week_end_date: str
    doctor_id: Optional[int]
    doctor_name: Optional[str]
    
    schedules: list[ScheduleDetailedResponse]
    total_working_days: int
    total_on_call_days: int
    total_hours: float


# Monthly Schedule Response
class MonthlyScheduleResponse(BaseModel):
    month: int
    year: int
    doctor_id: Optional[int]
    doctor_name: Optional[str]
    
    total_schedules: int
    working_days: int
    holidays: int
    leaves: int
    on_call_days: int
    
    schedules: list[ScheduleDetailedResponse]


# Bulk Schedule Create Schema
class BulkScheduleCreateSchema(BaseModel):
    doctor_id: int = Field(..., gt=0)
    start_date: str = Field(..., max_length=20)
    end_date: str = Field(..., max_length=20)
    
    shift_id: int = Field(..., gt=0)
    department_id: Optional[int] = None
    
    # Days to include
    include_weekends: bool = Field(default=False)
    exclude_dates: Optional[list[str]] = Field(None, description="Dates to exclude")
    
    # Specific days of week (0=Monday, 6=Sunday)
    specific_days: Optional[list[int]] = Field(None, description="Specific days of week")
    
    is_available: bool = Field(default=True)
    max_appointments: Optional[int] = Field(None, ge=0)
    
    notes: Optional[str] = None
    
    created_by: str = Field(..., max_length=200)


# Bulk Update Schema
class BulkScheduleUpdateSchema(BaseModel):
    schedule_ids: list[int] = Field(..., min_items=1)
    
    shift_id: Optional[int] = None
    is_available: Optional[bool] = None
    max_appointments: Optional[int] = None
    status: Optional[str] = None
    day_type: Optional[str] = None
    notes: Optional[str] = None
    
    updated_by: str = Field(..., max_length=200)


# Schedule Filter Schema
class ScheduleFilterSchema(BaseModel):
    doctor_id: Optional[int] = None
    shift_id: Optional[int] = None
    department_id: Optional[int] = None
    
    start_date: Optional[str] = Field(None, max_length=20)
    end_date: Optional[str] = Field(None, max_length=20)
    
    status: Optional[str] = Field(None, max_length=20)
    day_type: Optional[str] = Field(None, max_length=20)
    
    is_available: Optional[bool] = None
    is_on_call: Optional[bool] = None


# Schedule Conflict Check Schema
class ScheduleConflictCheckSchema(BaseModel):
    doctor_id: int = Field(..., gt=0)
    schedule_date: str = Field(..., max_length=20)
    start_time: str = Field(..., max_length=10)
    end_time: str = Field(..., max_length=10)
    
    exclude_schedule_id: Optional[int] = None


# Schedule Conflict Response
class ScheduleConflictResponse(BaseModel):
    has_conflict: bool
    conflict_details: Optional[dict]
    message: str


# Shift Swap Request Schema
class ShiftSwapRequestSchema(BaseModel):
    requester_schedule_id: int = Field(..., gt=0)
    target_schedule_id: int = Field(..., gt=0)
    
    requester_doctor_id: int = Field(..., gt=0)
    target_doctor_id: int = Field(..., gt=0)
    
    reason: str = Field(..., description="Reason for swap")
    notes: Optional[str] = None
    
    requested_by: str = Field(..., max_length=200)


# Shift Swap Approval Schema
class ShiftSwapApprovalSchema(BaseModel):
    is_approved: bool = Field(...)
    approved_by: str = Field(..., max_length=200)
    approval_date: str = Field(..., max_length=20)
    remarks: Optional[str] = None


# Schedule Coverage Schema
class ScheduleCoverageSchema(BaseModel):
    date: str
    department_id: Optional[int]
    shift_id: Optional[int]
    
    required_doctors: int
    scheduled_doctors: int
    available_doctors: int
    on_call_doctors: int
    
    is_fully_covered: bool
    coverage_percentage: float


# Doctor Availability Schema
class DoctorAvailabilitySchema(BaseModel):
    doctor_id: int
    doctor_name: str
    date: str
    
    is_scheduled: bool
    is_available: bool
    is_on_leave: bool
    is_on_call: bool
    
    shift_name: Optional[str]
    start_time: Optional[str]
    end_time: Optional[str]
    
    max_appointments: Optional[int]
    booked_appointments: int
    available_slots: Optional[int]


# Schedule Statistics Schema
class ScheduleStatisticsSchema(BaseModel):
    doctor_id: Optional[int]
    period_start: str
    period_end: str
    
    total_schedules: int
    working_days: int
    holidays: int
    weekends: int
    leaves: int
    on_call_days: int
    
    total_hours_worked: float
    average_hours_per_day: float
    
    total_appointments: int
    average_appointments_per_day: float


# Roster Template Schema
class RosterTemplateSchema(BaseModel):
    template_name: str = Field(..., max_length=100)
    department_id: Optional[int] = None
    
    # Weekly pattern
    monday_shift_id: Optional[int] = None
    tuesday_shift_id: Optional[int] = None
    wednesday_shift_id: Optional[int] = None
    thursday_shift_id: Optional[int] = None
    friday_shift_id: Optional[int] = None
    saturday_shift_id: Optional[int] = None
    sunday_shift_id: Optional[int] = None
    
    # Rotation details
    rotation_weeks: int = Field(default=1, ge=1, description="Number of weeks before rotation")
    
    is_active: bool = Field(default=True)
    created_by: str = Field(..., max_length=200)


# Apply Roster Template Schema
class ApplyRosterTemplateSchema(BaseModel):
    template_id: int = Field(..., gt=0)
    doctor_ids: list[int] = Field(..., min_items=1)
    
    start_date: str = Field(..., max_length=20)
    end_date: str = Field(..., max_length=20)
    
    override_existing: bool = Field(default=False)
    applied_by: str = Field(..., max_length=200)


# On-Call Schedule Schema
class OnCallScheduleSchema(BaseModel):
    doctor_id: int = Field(..., gt=0)
    on_call_date: str = Field(..., max_length=20)
    
    start_time: str = Field(..., max_length=10)
    end_time: str = Field(..., max_length=10)
    
    is_primary: bool = Field(default=True, description="Primary or backup on-call")
    
    department_id: Optional[int] = None
    specialty: Optional[str] = Field(None, max_length=100)
    
    contact_number: str = Field(..., max_length=20)
    backup_doctor_id: Optional[int] = None
    
    notes: Optional[str] = None
    scheduled_by: str = Field(..., max_length=200)


# Schedule Summary by Department
class DepartmentScheduleSummarySchema(BaseModel):
    department_id: int
    department_name: str
    date: str
    
    total_doctors_scheduled: int
    total_doctors_available: int
    total_doctors_on_leave: int
    total_doctors_on_call: int
    
    shifts_breakdown: dict  # {shift_name: count}
    
    is_adequately_staffed: bool
    staffing_percentage: float


# Schedule Notification Schema
class ScheduleNotificationSchema(BaseModel):
    schedule_id: int
    doctor_id: int
    notification_type: str = Field(..., description="created, updated, cancelled, reminder")
    
    send_email: bool = Field(default=True)
    send_sms: bool = Field(default=False)
    send_push: bool = Field(default=True)
    
    message: Optional[str] = None