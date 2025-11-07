"""
Attendance Schemas
Pydantic schemas for staff attendance tracking and management
"""

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, Any, List
from datetime import datetime, date, time, timedelta
from decimal import Decimal
from enum import Enum
import re


# Enums
class AttendanceStatus(str, Enum):
    """Valid attendance statuses"""
    PRESENT = "present"
    ABSENT = "absent"
    HALF_DAY = "half_day"
    ON_LEAVE = "on_leave"
    LATE = "late"
    EARLY_DEPARTURE = "early_departure"
    HOLIDAY = "holiday"
    WEEKEND = "weekend"


class CheckInMethod(str, Enum):
    """Valid check-in methods"""
    BIOMETRIC = "biometric"
    MANUAL = "manual"
    RFID = "rfid"
    MOBILE_APP = "mobile_app"
    WEB_PORTAL = "web_portal"
    FACE_RECOGNITION = "face_recognition"


class EmployeeType(str, Enum):
    """Employee types for attendance"""
    STAFF = "staff"
    DOCTOR = "doctor"
    NURSE = "nurse"


# Nested Schemas
class StaffBasic(BaseModel):
    """Basic staff info"""
    id: int
    full_name: str
    employee_id: str
    department: Optional[str] = None
    
    class Config:
        from_attributes = True


class DoctorBasic(BaseModel):
    """Basic doctor info"""
    id: int
    full_name: str
    employee_id: Optional[str] = None
    specialization: Optional[str] = None
    
    class Config:
        from_attributes = True


class NurseBasic(BaseModel):
    """Basic nurse info"""
    id: int
    full_name: str
    employee_id: Optional[str] = None
    ward: Optional[str] = None
    
    class Config:
        from_attributes = True


class ShiftBasic(BaseModel):
    """Basic shift info"""
    id: int
    shift_name: str
    start_time: str
    end_time: str
    duration_hours: Optional[float] = None
    
    class Config:
        from_attributes = True


# Time-related Schemas
class WorkHours(BaseModel):
    """Work hours details"""
    scheduled_minutes: int = Field(..., ge=0, description="Scheduled work minutes")
    actual_minutes: int = Field(..., ge=0, description="Actual work minutes")
    overtime_minutes: int = Field(default=0, ge=0, description="Overtime minutes")
    break_minutes: int = Field(default=0, ge=0, description="Break time minutes")
    
    @property
    def scheduled_hours(self) -> float:
        return round(self.scheduled_minutes / 60, 2)
    
    @property
    def actual_hours(self) -> float:
        return round(self.actual_minutes / 60, 2)
    
    @property
    def overtime_hours(self) -> float:
        return round(self.overtime_minutes / 60, 2)
    
    class Config:
        json_schema_extra = {
            "example": {
                "scheduled_minutes": 480,  # 8 hours
                "actual_minutes": 495,     # 8.25 hours
                "overtime_minutes": 15,    # 15 minutes
                "break_minutes": 60        # 1 hour
            }
        }


class TimingDetails(BaseModel):
    """Check-in/check-out timing details"""
    check_in_time: str = Field(..., description="Check-in time (HH:MM)")
    check_out_time: Optional[str] = Field(None, description="Check-out time (HH:MM)")
    is_late: bool = Field(default=False, description="Is late arrival")
    late_by_minutes: Optional[int] = Field(None, ge=0, description="Late by minutes")
    is_early_departure: bool = Field(default=False, description="Is early departure")
    early_by_minutes: Optional[int] = Field(None, ge=0, description="Early by minutes")
    
    @field_validator('check_in_time', 'check_out_time')
    @classmethod
    def validate_time_format(cls, v):
        """Validate time format"""
        if v is None:
            return None
        try:
            datetime.strptime(v, '%H:%M')
            return v
        except ValueError:
            raise ValueError("Time must be in HH:MM format")
    
    class Config:
        json_schema_extra = {
            "example": {
                "check_in_time": "09:15",
                "check_out_time": "18:00",
                "is_late": True,
                "late_by_minutes": 15,
                "is_early_departure": False,
                "early_by_minutes": None
            }
        }


# Base Schema
class AttendanceBase(BaseModel):
    """Base schema with common fields"""
    # Date
    attendance_date: str = Field(..., description="Attendance date (YYYY-MM-DD)")
    
    # Employee Reference (at least one required)
    staff_id: Optional[int] = Field(None, description="Staff ID")
    doctor_id: Optional[int] = Field(None, description="Doctor ID")
    nurse_id: Optional[int] = Field(None, description="Nurse ID")
    
    # Employee Info (denormalized)
    employee_name: str = Field(..., max_length=200, description="Employee name")
    employee_id: str = Field(..., max_length=50, description="Employee ID/number")
    
    # Timing
    check_in_time: Optional[str] = Field(None, description="Check-in time (HH:MM)")
    check_out_time: Optional[str] = Field(None, description="Check-out time (HH:MM)")
    
    # Work Hours (in minutes)
    scheduled_hours: Optional[int] = Field(None, ge=0, description="Scheduled work minutes")
    actual_hours: Optional[int] = Field(None, ge=0, description="Actual work minutes")
    overtime_hours: Optional[int] = Field(default=0, ge=0, description="Overtime minutes")
    
    # Shift
    shift_id: Optional[int] = Field(None, description="Shift ID")
    shift_name: Optional[str] = Field(None, max_length=50, description="Shift name")
    
    # Status
    status: AttendanceStatus = Field(..., description="Attendance status")
    
    # Late/Early
    is_late: bool = Field(default=False, description="Late arrival")
    late_by_minutes: Optional[int] = Field(None, ge=0, description="Minutes late")
    is_early_departure: bool = Field(default=False, description="Early departure")
    early_by_minutes: Optional[int] = Field(None, ge=0, description="Minutes early departure")
    
    # Location
    check_in_location: Optional[str] = Field(None, max_length=200, description="Check-in location")
    check_out_location: Optional[str] = Field(None, max_length=200, description="Check-out location")
    
    # Method
    check_in_method: Optional[CheckInMethod] = Field(None, description="Check-in method")
    check_out_method: Optional[CheckInMethod] = Field(None, description="Check-out method")
    
    # Break Time
    total_break_minutes: Optional[int] = Field(default=0, ge=0, description="Total break minutes")
    
    # Approval
    approved_by: Optional[str] = Field(None, max_length=200, description="Approved by")
    approval_date: Optional[str] = Field(None, description="Approval date")
    
    # Notes
    notes: Optional[str] = Field(None, description="Notes")
    remarks: Optional[str] = Field(None, description="Remarks")

    @field_validator('attendance_date', 'approval_date')
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
    
    @field_validator('check_in_time', 'check_out_time')
    @classmethod
    def validate_time_format(cls, v):
        """Validate time format"""
        if v is None:
            return None
        try:
            datetime.strptime(v, '%H:%M')
            return v
        except ValueError:
            raise ValueError("Time must be in HH:MM format")
    
    @model_validator(mode='after')
    def validate_employee_reference(self):
        """Ensure at least one employee reference is provided"""
        if not any([self.staff_id, self.doctor_id, self.nurse_id]):
            raise ValueError("At least one of staff_id, doctor_id, or nurse_id must be provided")
        return self
    
    @model_validator(mode='after')
    def validate_checkout_after_checkin(self):
        """Ensure check-out is after check-in"""
        if self.check_in_time and self.check_out_time:
            try:
                checkin = datetime.strptime(self.check_in_time, '%H:%M')
                checkout = datetime.strptime(self.check_out_time, '%H:%M')
                if checkout < checkin:
                    raise ValueError("Check-out time must be after check-in time")
            except ValueError:
                pass
        return self
    
    @model_validator(mode='after')
    def validate_late_status(self):
        """Ensure late status is consistent with late_by_minutes"""
        if self.is_late and not self.late_by_minutes:
            raise ValueError("late_by_minutes required when is_late is True")
        return self


# Create Schema
class AttendanceCreate(AttendanceBase):
    """Schema for creating attendance record"""
    
    class Config:
        json_schema_extra = {
            "example": {
                "attendance_date": "2024-01-15",
                "staff_id": 123,
                "employee_name": "John Doe",
                "employee_id": "EMP-001",
                "check_in_time": "09:15",
                "check_out_time": "18:00",
                "scheduled_hours": 480,
                "actual_hours": 495,
                "overtime_hours": 15,
                "shift_id": 1,
                "shift_name": "Morning Shift",
                "status": "present",
                "is_late": True,
                "late_by_minutes": 15,
                "check_in_method": "biometric",
                "check_out_method": "biometric",
                "check_in_location": "Main Building",
                "total_break_minutes": 60,
                "notes": "Traffic delay"
            }
        }


# Update Schema
class AttendanceUpdate(BaseModel):
    """Schema for updating attendance (partial updates allowed)"""
    check_in_time: Optional[str] = None
    check_out_time: Optional[str] = None
    scheduled_hours: Optional[int] = Field(None, ge=0)
    actual_hours: Optional[int] = Field(None, ge=0)
    overtime_hours: Optional[int] = Field(None, ge=0)
    shift_id: Optional[int] = None
    shift_name: Optional[str] = None
    status: Optional[AttendanceStatus] = None
    is_late: Optional[bool] = None
    late_by_minutes: Optional[int] = Field(None, ge=0)
    is_early_departure: Optional[bool] = None
    early_by_minutes: Optional[int] = Field(None, ge=0)
    check_in_location: Optional[str] = None
    check_out_location: Optional[str] = None
    check_in_method: Optional[CheckInMethod] = None
    check_out_method: Optional[CheckInMethod] = None
    total_break_minutes: Optional[int] = Field(None, ge=0)
    approved_by: Optional[str] = None
    approval_date: Optional[str] = None
    notes: Optional[str] = None
    remarks: Optional[str] = None

    @field_validator('check_in_time', 'check_out_time')
    @classmethod
    def validate_time_format(cls, v):
        if v is None:
            return None
        try:
            datetime.strptime(v, '%H:%M')
            return v
        except ValueError:
            raise ValueError("Time must be in HH:MM format")


# Response Schema
class AttendanceResponse(AttendanceBase):
    """Schema for attendance response"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "attendance_date": "2024-01-15",
                "employee_name": "John Doe",
                "employee_id": "EMP-001",
                "check_in_time": "09:15",
                "check_out_time": "18:00",
                "status": "present",
                "is_late": True,
                "late_by_minutes": 15,
                "actual_hours": 495,
                "overtime_hours": 15,
                "created_at": "2024-01-15T09:15:00",
                "updated_at": "2024-01-15T18:00:00"
            }
        }


# Detailed Response with Relationships
class AttendanceDetailResponse(AttendanceResponse):
    """Detailed attendance response with nested relationships"""
    staff: Optional[StaffBasic] = None
    doctor: Optional[DoctorBasic] = None
    nurse: Optional[NurseBasic] = None
    shift: Optional[ShiftBasic] = None
    
    class Config:
        from_attributes = True


# List Response Schema
class AttendanceListResponse(BaseModel):
    """Schema for paginated list of attendance records"""
    total: int = Field(..., description="Total number of records")
    page: int = Field(..., ge=1, description="Current page number")
    page_size: int = Field(..., ge=1, le=100, description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")
    items: List[AttendanceResponse] = Field(..., description="Attendance items")


# Filter/Query Schema
class AttendanceFilter(BaseModel):
    """Schema for filtering attendance records"""
    # Employee filters
    staff_id: Optional[int] = Field(None, description="Filter by staff ID")
    doctor_id: Optional[int] = Field(None, description="Filter by doctor ID")
    nurse_id: Optional[int] = Field(None, description="Filter by nurse ID")
    employee_id: Optional[str] = Field(None, description="Filter by employee ID")
    employee_name: Optional[str] = Field(None, description="Filter by employee name")
    
    # Date filters
    attendance_date: Optional[str] = Field(None, description="Specific date (YYYY-MM-DD)")
    date_from: Optional[str] = Field(None, description="Date range from (YYYY-MM-DD)")
    date_to: Optional[str] = Field(None, description="Date range to (YYYY-MM-DD)")
    month: Optional[int] = Field(None, ge=1, le=12, description="Filter by month")
    year: Optional[int] = Field(None, ge=2000, le=2100, description="Filter by year")
    
    # Status filters
    status: Optional[AttendanceStatus] = Field(None, description="Filter by status")
    is_late: Optional[bool] = Field(None, description="Filter late arrivals")
    is_early_departure: Optional[bool] = Field(None, description="Filter early departures")
    has_overtime: Optional[bool] = Field(None, description="Filter with overtime")
    
    # Shift filter
    shift_id: Optional[int] = Field(None, description="Filter by shift")
    
    # Approval filter
    approval_status: Optional[str] = Field(None, description="approved, pending, rejected")
    
    # Method filter
    check_in_method: Optional[CheckInMethod] = Field(None, description="Filter by check-in method")
    
    # Pagination
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")
    
    # Sorting
    sort_by: Optional[str] = Field("attendance_date", description="Field to sort by")
    sort_order: Optional[str] = Field("desc", pattern="^(asc|desc)$", description="Sort order")
    
    # Include relationships
    include_employee: bool = Field(False, description="Include employee details")
    include_shift: bool = Field(False, description="Include shift details")


# Check-in Schema
class CheckIn(BaseModel):
    """Schema for checking in"""
    attendance_date: str = Field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d'), description="Date")
    employee_id: str = Field(..., description="Employee ID")
    employee_type: EmployeeType = Field(..., description="Employee type")
    check_in_time: str = Field(default_factory=lambda: datetime.now().strftime('%H:%M'), description="Check-in time")
    check_in_method: CheckInMethod = Field(default=CheckInMethod.MANUAL, description="Check-in method")
    check_in_location: Optional[str] = Field(None, description="Check-in location")
    latitude: Optional[float] = Field(None, description="GPS latitude")
    longitude: Optional[float] = Field(None, description="GPS longitude")
    device_id: Optional[str] = Field(None, description="Device identifier")
    notes: Optional[str] = Field(None, description="Check-in notes")
    
    @field_validator('check_in_time')
    @classmethod
    def validate_time(cls, v):
        try:
            datetime.strptime(v, '%H:%M')
            return v
        except ValueError:
            raise ValueError("Time must be in HH:MM format")
    
    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": "EMP-001",
                "employee_type": "staff",
                "check_in_time": "09:15",
                "check_in_method": "mobile_app",
                "check_in_location": "Main Building",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "notes": "Morning shift"
            }
        }


# Check-out Schema
class CheckOut(BaseModel):
    """Schema for checking out"""
    check_out_time: str = Field(default_factory=lambda: datetime.now().strftime('%H:%M'), description="Check-out time")
    check_out_method: CheckInMethod = Field(default=CheckInMethod.MANUAL, description="Check-out method")
    check_out_location: Optional[str] = Field(None, description="Check-out location")
    latitude: Optional[float] = Field(None, description="GPS latitude")
    longitude: Optional[float] = Field(None, description="GPS longitude")
    total_break_minutes: Optional[int] = Field(None, ge=0, description="Total break time")
    work_summary: Optional[str] = Field(None, description="Work summary")
    notes: Optional[str] = Field(None, description="Check-out notes")
    
    @field_validator('check_out_time')
    @classmethod
    def validate_time(cls, v):
        try:
            datetime.strptime(v, '%H:%M')
            return v
        except ValueError:
            raise ValueError("Time must be in HH:MM format")
    
    class Config:
        json_schema_extra = {
            "example": {
                "check_out_time": "18:00",
                "check_out_method": "mobile_app",
                "check_out_location": "Main Building",
                "total_break_minutes": 60,
                "work_summary": "Completed all assigned tasks",
                "notes": "Normal shift"
            }
        }


# Manual Attendance Entry Schema
class ManualAttendanceEntry(BaseModel):
    """Schema for manual attendance entry by admin"""
    attendance_date: str = Field(..., description="Attendance date")
    employee_id: str = Field(..., description="Employee ID")
    employee_type: EmployeeType = Field(..., description="Employee type")
    status: AttendanceStatus = Field(..., description="Attendance status")
    check_in_time: Optional[str] = Field(None, description="Check-in time")
    check_out_time: Optional[str] = Field(None, description="Check-out time")
    shift_id: Optional[int] = Field(None, description="Shift ID")
    notes: str = Field(..., description="Reason/notes for manual entry")
    entered_by: str = Field(..., description="Admin who entered the record")
    
    @field_validator('attendance_date')
    @classmethod
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")


# Regularization Request Schema
class AttendanceRegularization(BaseModel):
    """Schema for attendance regularization request"""
    attendance_id: int = Field(..., description="Attendance record ID")
    requested_check_in: Optional[str] = Field(None, description="Requested check-in time")
    requested_check_out: Optional[str] = Field(None, description="Requested check-out time")
    requested_status: Optional[AttendanceStatus] = Field(None, description="Requested status")
    reason: str = Field(..., min_length=10, description="Reason for regularization")
    supporting_documents: Optional[List[str]] = Field(None, description="Document URLs")
    
    class Config:
        json_schema_extra = {
            "example": {
                "attendance_id": 123,
                "requested_check_in": "09:00",
                "requested_check_out": "18:00",
                "reason": "Biometric system was down, manually verified by supervisor",
                "supporting_documents": ["/uploads/supervisor_approval.pdf"]
            }
        }


# Approval Schema
class ApproveAttendance(BaseModel):
    """Schema for approving attendance"""
    approved: bool = Field(..., description="Approval status")
    approved_by: str = Field(..., description="Approver name/ID")
    approval_notes: Optional[str] = Field(None, description="Approval notes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "approved": True,
                "approved_by": "Manager John",
                "approval_notes": "Verified and approved"
            }
        }


# Statistics Schema
class AttendanceStats(BaseModel):
    """Schema for attendance statistics"""
    total_records: int
    present_count: int
    absent_count: int
    half_day_count: int
    on_leave_count: int
    late_count: int
    early_departure_count: int
    average_work_hours: Optional[float] = None
    total_overtime_hours: Optional[float] = None
    attendance_percentage: Optional[float] = None
    punctuality_percentage: Optional[float] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_records": 22,
                "present_count": 20,
                "absent_count": 1,
                "half_day_count": 0,
                "on_leave_count": 1,
                "late_count": 3,
                "early_departure_count": 1,
                "average_work_hours": 8.2,
                "total_overtime_hours": 5.5,
                "attendance_percentage": 95.45,
                "punctuality_percentage": 86.36
            }
        }


# Monthly Report Schema
class MonthlyAttendanceReport(BaseModel):
    """Schema for monthly attendance report"""
    employee_id: str
    employee_name: str
    month: int
    year: int
    total_working_days: int
    days_present: int
    days_absent: int
    days_on_leave: int
    days_half_day: int
    late_arrivals: int
    early_departures: int
    total_work_hours: float
    total_overtime_hours: float
    attendance_percentage: float
    status_breakdown: dict[str, int]
    
    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": "EMP-001",
                "employee_name": "John Doe",
                "month": 1,
                "year": 2024,
                "total_working_days": 22,
                "days_present": 20,
                "days_absent": 1,
                "days_on_leave": 1,
                "days_half_day": 0,
                "late_arrivals": 3,
                "early_departures": 1,
                "total_work_hours": 164.5,
                "total_overtime_hours": 5.5,
                "attendance_percentage": 95.45,
                "status_breakdown": {
                    "present": 20,
                    "absent": 1,
                    "on_leave": 1
                }
            }
        }


# Dashboard Schema
class AttendanceDashboard(BaseModel):
    """Dashboard summary for attendance"""
    today_present: int
    today_absent: int
    today_on_leave: int
    today_late: int
    currently_checked_in: int
    yet_to_check_in: int
    checked_out: int
    overtime_today: int
    month_attendance_rate: float
    month_punctuality_rate: float
    top_late_employees: List[dict[str, Any]]
    department_wise_attendance: dict[str, dict[str, int]]
    
    class Config:
        json_schema_extra = {
            "example": {
                "today_present": 145,
                "today_absent": 8,
                "today_on_leave": 12,
                "today_late": 15,
                "currently_checked_in": 120,
                "yet_to_check_in": 25,
                "checked_out": 20,
                "overtime_today": 8,
                "month_attendance_rate": 94.5,
                "month_punctuality_rate": 87.3,
                "top_late_employees": [
                    {"employee_id": "EMP-001", "late_count": 5}
                ],
                "department_wise_attendance": {
                    "Nursing": {"present": 50, "absent": 3},
                    "Admin": {"present": 30, "absent": 2}
                }
            }
        }


# Timesheet Schema
class EmployeeTimesheet(BaseModel):
    """Employee timesheet for a period"""
    employee_id: str
    employee_name: str
    start_date: str
    end_date: str
    records: List[dict[str, Any]]
    summary: dict[str, Any]
    
    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": "EMP-001",
                "employee_name": "John Doe",
                "start_date": "2024-01-01",
                "end_date": "2024-01-31",
                "records": [
                    {
                        "date": "2024-01-15",
                        "check_in": "09:00",
                        "check_out": "18:00",
                        "hours": 8.0,
                        "status": "present"
                    }
                ],
                "summary": {
                    "total_days": 22,
                    "present": 20,
                    "absent": 1,
                    "total_hours": 164.5
                }
            }
        }


# Bulk Import Schema
class BulkAttendanceImport(BaseModel):
    """Schema for bulk importing attendance"""
    records: List[AttendanceCreate] = Field(..., min_length=1, max_length=1000)
    import_date: str = Field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d'))
    imported_by: str = Field(..., description="User who imported")
    
    class Config:
        json_schema_extra = {
            "example": {
                "records": [
                    {
                        "attendance_date": "2024-01-15",
                        "employee_id": "EMP-001",
                        "employee_name": "John Doe",
                        "status": "present",
                        "check_in_time": "09:00",
                        "check_out_time": "18:00"
                    }
                ],
                "imported_by": "Admin"
            }
        }


# Leave Integration Schema
class LeaveAttendance(BaseModel):
    """Schema for marking leave in attendance"""
    employee_id: str
    leave_start_date: str
    leave_end_date: str
    leave_type: str = Field(..., description="sick, casual, annual, etc.")
    leave_reason: Optional[str] = None
    half_day: bool = Field(default=False, description="Half day leave")
    
    @field_validator('leave_start_date', 'leave_end_date')
    @classmethod
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
    
    @model_validator(mode='after')
    def validate_date_range(self):
        start = datetime.strptime(self.leave_start_date, '%Y-%m-%d')
        end = datetime.strptime(self.leave_end_date, '%Y-%m-%d')
        if end < start:
            raise ValueError("End date must be after start date")
        return self


# Shift-wise Summary
class ShiftAttendanceSummary(BaseModel):
    """Attendance summary by shift"""
    shift_id: int
    shift_name: str
    date: str
    total_employees: int
    present: int
    absent: int
    late: int
    on_time: int
    attendance_rate: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "shift_id": 1,
                "shift_name": "Morning Shift",
                "date": "2024-01-15",
                "total_employees": 50,
                "present": 47,
                "absent": 3,
                "late": 5,
                "on_time": 42,
                "attendance_rate": 94.0
            }
        }


# Overtime Request Schema
class OvertimeRequest(BaseModel):
    """Schema for overtime request"""
    attendance_id: int
    overtime_hours: int = Field(..., gt=0, description="Overtime hours in minutes")
    reason: str = Field(..., min_length=10, description="Reason for overtime")
    approved_by_supervisor: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "attendance_id": 123,
                "overtime_hours": 120,
                "reason": "Project deadline - urgent delivery",
                "approved_by_supervisor": "Manager John"
            }
        }