"""
Event Schemas
Pydantic schemas for hospital events, meetings, and activities
"""

from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict, EmailStr
from typing import Optional, List, Dict, Any, Union
from datetime import datetime, time, timedelta
from enum import Enum
import json
import re


# Enums
class EventType(str, Enum):
    """Valid event types"""
    MEETING = "meeting"
    TRAINING = "training"
    SEMINAR = "seminar"
    CONFERENCE = "conference"
    HEALTH_CAMP = "health_camp"
    AWARENESS = "awareness"
    CELEBRATION = "celebration"
    WORKSHOP = "workshop"
    WEBINAR = "webinar"


class EventStatus(str, Enum):
    """Event status"""
    SCHEDULED = "scheduled"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    POSTPONED = "postponed"


class EventPriority(str, Enum):
    """Event priority"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class TargetAudience(str, Enum):
    """Target audience types"""
    STAFF = "staff"
    DOCTORS = "doctors"
    NURSES = "nurses"
    PATIENTS = "patients"
    PUBLIC = "public"
    ALL = "all"


# Helper Schemas
class DepartmentBasic(BaseModel):
    """Basic department info"""
    id: int
    name: str
    head_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class EventParticipant(BaseModel):
    """Event participant information"""
    name: str = Field(..., max_length=200, description="Participant name")
    email: Optional[EmailStr] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, max_length=20, description="Phone number")
    designation: Optional[str] = Field(None, max_length=100, description="Job designation")
    department: Optional[str] = Field(None, max_length=100, description="Department")
    organization: Optional[str] = Field(None, max_length=200, description="Organization (external participants)")
    registration_date: datetime = Field(default_factory=datetime.utcnow)
    attendance_status: Optional[str] = Field(None, pattern="^(registered|confirmed|attended|absent|cancelled)$")
    notes: Optional[str] = Field(None, description="Participant notes")
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if v is None:
            return None
        cleaned = re.sub(r'[\s\-\(\)]', '', v)
        if not re.match(r'^\+?[0-9]{10,15}$', cleaned):
            raise ValueError("Invalid phone number format")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Dr. John Doe",
                "email": "john.doe@hospital.com",
                "phone": "+1-555-123-4567",
                "designation": "Senior Cardiologist",
                "department": "Cardiology",
                "attendance_status": "registered"
            }
        }


class EventResource(BaseModel):
    """Required resource"""
    resource_name: str = Field(..., description="Resource name")
    quantity: int = Field(default=1, gt=0, description="Quantity needed")
    assigned: bool = Field(default=False, description="Whether assigned")
    assigned_to: Optional[str] = Field(None, description="Who it's assigned to")
    notes: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "resource_name": "Projector",
                "quantity": 1,
                "assigned": True,
                "assigned_to": "IT Department"
            }
        }


class AgendaItem(BaseModel):
    """Agenda item"""
    time: str = Field(..., pattern="^([01][0-9]|2[0-3]):[0-5][0-9]$", description="Time (HH:MM)")
    topic: str = Field(..., max_length=200, description="Topic/subject")
    duration_minutes: int = Field(..., gt=0, le=480, description="Duration in minutes")
    speaker: Optional[str] = Field(None, max_length=200, description="Speaker/presenter")
    description: Optional[str] = Field(None, description="Detailed description")
    
    class Config:
        json_schema_extra = {
            "example": {
                "time": "10:00",
                "topic": "Welcome and Opening Remarks",
                "duration_minutes": 15,
                "speaker": "Dr. Jane Smith, Chief Medical Officer"
            }
        }


# Base Schema
class EventBase(BaseModel):
    """Base schema for events"""
    event_code: str = Field(..., max_length=20, description="Unique event code")
    title: str = Field(..., min_length=3, max_length=200, description="Event title")
    description: str = Field(..., min_length=10, description="Detailed description")
    event_type: EventType = Field(..., description="Type of event")
    event_date: str = Field(..., description="Event date (YYYY-MM-DD)")
    start_time: str = Field(..., pattern="^([01][0-9]|2[0-3]):[0-5][0-9]$", description="Start time (HH:MM)")
    end_time: str = Field(..., pattern="^([01][0-9]|2[0-3]):[0-5][0-9]$", description="End time (HH:MM)")
    duration_hours: Optional[int] = Field(None, ge=0, le=24, description="Duration in hours")
    location: str = Field(..., max_length=200, description="Event location")
    venue: Optional[str] = Field(None, max_length=200, description="Specific venue name")
    floor_number: Optional[int] = Field(None, description="Floor number")
    organizer: str = Field(..., max_length=200, description="Event organizer")
    contact_person: Optional[str] = Field(None, max_length=200, description="Contact person")
    contact_phone: Optional[str] = Field(None, max_length=20, description="Contact phone")
    department_id: Optional[int] = Field(None, description="Department ID")
    max_participants: Optional[int] = Field(None, gt=0, description="Maximum participants")
    registered_participants: int = Field(default=0, ge=0, description="Registered count")
    requires_registration: bool = Field(default=False, description="Registration required")
    registration_deadline: Optional[str] = Field(None, description="Registration deadline (YYYY-MM-DD)")
    status: EventStatus = Field(default=EventStatus.SCHEDULED, description="Event status")
    priority: EventPriority = Field(default=EventPriority.NORMAL, description="Priority level")
    is_public: bool = Field(default=False, description="Public event")
    target_audience: Optional[str] = Field(None, max_length=200, description="Target audience")
    resources_required: Optional[str] = Field(None, description="Required resources")
    notes: Optional[str] = Field(None, description="Additional notes")
    agenda: Optional[str] = Field(None, description="Event agenda")
    attachment_url: Optional[str] = Field(None, max_length=500, description="Attachment URL")

    @field_validator('event_date', 'registration_deadline')
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
    
    @field_validator('contact_phone')
    @classmethod
    def validate_phone(cls, v):
        """Validate phone number"""
        if v is None:
            return None
        cleaned = re.sub(r'[\s\-\(\)]', '', v)
        if not re.match(r'^\+?[0-9]{10,15}$', cleaned):
            raise ValueError("Invalid phone number format")
        return v
    
    @model_validator(mode='after')
    def validate_times_and_dates(self):
        """Validate times and calculate duration"""
        # Validate time range
        if self.start_time and self.end_time:
            start = datetime.strptime(self.start_time, '%H:%M')
            end = datetime.strptime(self.end_time, '%H:%M')
            
            if end <= start:
                raise ValueError("End time must be after start time")
            
            # Auto-calculate duration if not provided
            if not self.duration_hours:
                duration = (end - start).total_seconds() / 3600
                self.duration_hours = round(duration, 1)
        
        # Validate registration deadline
        if self.requires_registration and not self.registration_deadline:
            raise ValueError("Registration deadline required when registration is enabled")
        
        if self.registration_deadline and self.event_date:
            deadline = datetime.strptime(self.registration_deadline, '%Y-%m-%d')
            event_date = datetime.strptime(self.event_date, '%Y-%m-%d')
            if deadline > event_date:
                raise ValueError("Registration deadline must be before event date")
        
        # Validate participant count
        if self.max_participants and self.registered_participants > self.max_participants:
            raise ValueError("Registered participants cannot exceed maximum capacity")
        
        return self


# Create Schema
class EventCreate(BaseModel):
    """Schema for creating new event"""
    title: str = Field(..., min_length=3, max_length=200)
    description: str = Field(..., min_length=10)
    event_type: EventType
    event_date: str = Field(..., description="YYYY-MM-DD")
    start_time: str = Field(..., pattern="^([01][0-9]|2[0-3]):[0-5][0-9]$")
    end_time: str = Field(..., pattern="^([01][0-9]|2[0-3]):[0-5][0-9]$")
    location: str = Field(..., max_length=200)
    venue: Optional[str] = Field(None, max_length=200)
    floor_number: Optional[int] = None
    organizer: str = Field(..., max_length=200)
    contact_person: Optional[str] = Field(None, max_length=200)
    contact_phone: Optional[str] = Field(None, max_length=20)
    department_id: Optional[int] = None
    max_participants: Optional[int] = Field(None, gt=0)
    requires_registration: bool = Field(default=False)
    registration_deadline: Optional[str] = None
    priority: EventPriority = Field(default=EventPriority.NORMAL)
    is_public: bool = Field(default=False)
    target_audience: Optional[str] = None
    resources_required: Optional[str] = None
    agenda: Optional[str] = None
    notes: Optional[str] = None
    event_code: Optional[str] = None  # Auto-generated if not provided
    
    # Structured agenda
    agenda_items: Optional[List[AgendaItem]] = Field(None, description="Structured agenda")
    
    # Resources
    resource_list: Optional[List[EventResource]] = Field(None, description="Required resources")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Monthly Clinical Staff Meeting",
                "description": "Regular monthly meeting to discuss clinical updates and patient care protocols",
                "event_type": "meeting",
                "event_date": "2024-02-15",
                "start_time": "10:00",
                "end_time": "12:00",
                "location": "Conference Room A",
                "venue": "Main Building",
                "floor_number": 3,
                "organizer": "Medical Department",
                "contact_person": "Dr. Jane Smith",
                "contact_phone": "+1-555-987-6543",
                "max_participants": 50,
                "requires_registration": True,
                "registration_deadline": "2024-02-13",
                "priority": "normal",
                "is_public": False,
                "target_audience": "doctors, nurses"
            }
        }


# Update Schema
class EventUpdate(BaseModel):
    """Schema for updating event"""
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, min_length=10)
    event_type: Optional[EventType] = None
    event_date: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    location: Optional[str] = None
    venue: Optional[str] = None
    floor_number: Optional[int] = None
    organizer: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    status: Optional[EventStatus] = None
    priority: Optional[EventPriority] = None
    max_participants: Optional[int] = Field(None, gt=0)
    registration_deadline: Optional[str] = None
    is_public: Optional[bool] = None
    target_audience: Optional[str] = None
    resources_required: Optional[str] = None
    agenda: Optional[str] = None
    notes: Optional[str] = None


# Response Schema
class EventResponse(EventBase):
    """Schema for event response"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    # Calculated fields
    days_until_event: Optional[int] = Field(None, description="Days until event")
    is_upcoming: bool = Field(default=False, description="Is upcoming (within 7 days)")
    is_past: bool = Field(default=False, description="Event has passed")
    is_today: bool = Field(default=False, description="Event is today")
    seats_available: Optional[int] = Field(None, description="Available seats")
    occupancy_rate: Optional[float] = Field(None, description="Percentage filled")
    can_register: bool = Field(default=True, description="Registration still open")
    
    model_config = ConfigDict(from_attributes=True)
    
    @model_validator(mode='after')
    def calculate_event_status(self):
        """Calculate event-related status fields"""
        if self.event_date:
            event_dt = datetime.strptime(self.event_date, '%Y-%m-%d')
            today = datetime.now()
            
            # Calculate days
            delta = (event_dt.date() - today.date()).days
            self.days_until_event = delta
            
            # Status flags
            self.is_today = delta == 0
            self.is_upcoming = 0 <= delta <= 7
            self.is_past = delta < 0
        
        # Calculate seats
        if self.max_participants:
            self.seats_available = max(0, self.max_participants - self.registered_participants)
            self.occupancy_rate = round((self.registered_participants / self.max_participants) * 100, 2)
        
        # Can register?
        if self.requires_registration:
            if self.registration_deadline:
                deadline = datetime.strptime(self.registration_deadline, '%Y-%m-%d')
                self.can_register = deadline.date() >= datetime.now().date()
            
            # Check if full
            if self.max_participants and self.registered_participants >= self.max_participants:
                self.can_register = False
            
            # Check status
            if self.status in [EventStatus.CANCELLED, EventStatus.COMPLETED]:
                self.can_register = False
        
        return self
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "event_code": "EVT-2024-0001",
                "title": "Monthly Clinical Staff Meeting",
                "description": "Regular monthly meeting",
                "event_type": "meeting",
                "event_date": "2024-02-15",
                "start_time": "10:00",
                "end_time": "12:00",
                "location": "Conference Room A",
                "organizer": "Medical Department",
                "status": "scheduled",
                "registered_participants": 35,
                "max_participants": 50,
                "seats_available": 15,
                "days_until_event": 5,
                "is_upcoming": True,
                "can_register": True,
                "created_at": "2024-01-15T10:00:00",
                "updated_at": "2024-01-15T10:00:00"
            }
        }


# Detail Response with Relationships
class EventDetailResponse(EventResponse):
    """Detailed event response with relationships"""
    department: Optional[DepartmentBasic] = None
    participants: Optional[List[EventParticipant]] = Field(None, description="List of participants")
    agenda_items: Optional[List[AgendaItem]] = Field(None, description="Structured agenda")
    resources: Optional[List[EventResource]] = Field(None, description="Resources")
    
    model_config = ConfigDict(from_attributes=True)


# List Response Schema
class EventListResponse(BaseModel):
    """Schema for paginated list of events"""
    total: int = Field(..., description="Total number of records")
    page: int = Field(..., ge=1, description="Current page number")
    page_size: int = Field(..., ge=1, le=100, description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")
    items: List[EventResponse] = Field(..., description="Event items")
    summary: Optional[Dict[str, Any]] = Field(None, description="Summary statistics")


# Filter Schema
class EventFilter(BaseModel):
    """Schema for filtering events"""
    # Type and status filters
    event_type: Optional[Union[EventType, List[EventType]]] = Field(None, description="Filter by event type")
    status: Optional[Union[EventStatus, List[EventStatus]]] = Field(None, description="Filter by status")
    priority: Optional[EventPriority] = Field(None, description="Filter by priority")
    
    # Department filter
    department_id: Optional[int] = Field(None, description="Filter by department")
    
    # Date filters
    event_date: Optional[str] = Field(None, description="Specific date")
    event_date_from: Optional[str] = Field(None, description="From date")
    event_date_to: Optional[str] = Field(None, description="To date")
    
    # Boolean filters
    is_public: Optional[bool] = Field(None, description="Public events only")
    requires_registration: Optional[bool] = Field(None, description="Registration required")
    has_seats_available: Optional[bool] = Field(None, description="Has available seats")
    
    # Special filters
    upcoming_only: Optional[bool] = Field(None, description="Only upcoming events")
    today_only: Optional[bool] = Field(None, description="Only today's events")
    this_week: Optional[bool] = Field(None, description="Events this week")
    this_month: Optional[bool] = Field(None, description="Events this month")
    
    # Search
    search: Optional[str] = Field(None, description="Search in title, description")
    organizer: Optional[str] = Field(None, description="Filter by organizer")
    location: Optional[str] = Field(None, description="Filter by location")
    
    # Pagination
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")
    
    # Sorting
    sort_by: str = Field("event_date", description="Field to sort by")
    sort_order: str = Field("asc", pattern="^(asc|desc)$", description="Sort order")
    
    # Include relationships
    include_department: bool = Field(False, description="Include department details")
    include_participants: bool = Field(False, description="Include participant list")

    @field_validator('event_date', 'event_date_from', 'event_date_to')
    @classmethod
    def validate_date(cls, v):
        if v is None:
            return None
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")


# Registration Schema
class RegisterForEvent(BaseModel):
    """Schema for event registration"""
    participant: EventParticipant = Field(..., description="Participant information")
    send_confirmation: bool = Field(default=True, description="Send confirmation email")
    
    class Config:
        json_schema_extra = {
            "example": {
                "participant": {
                    "name": "Dr. John Doe",
                    "email": "john.doe@hospital.com",
                    "phone": "+1-555-123-4567",
                    "designation": "Senior Cardiologist",
                    "department": "Cardiology"
                },
                "send_confirmation": True
            }
        }


# Cancel Registration Schema
class CancelRegistration(BaseModel):
    """Schema for cancelling registration"""
    participant_email: EmailStr = Field(..., description="Participant email")
    cancellation_reason: Optional[str] = Field(None, description="Reason for cancellation")


# Mark Attendance Schema
class MarkAttendance(BaseModel):
    """Schema for marking attendance"""
    participant_email: EmailStr = Field(..., description="Participant email")
    attended: bool = Field(..., description="Whether attended")
    check_in_time: Optional[str] = Field(None, description="Check-in time")
    notes: Optional[str] = Field(None, description="Attendance notes")


# Cancel Event Schema
class CancelEvent(BaseModel):
    """Schema for cancelling event"""
    cancellation_reason: str = Field(..., min_length=10, description="Reason for cancellation")
    cancelled_by: str = Field(..., description="Who cancelled")
    notify_participants: bool = Field(default=True, description="Notify registered participants")
    refund_applicable: bool = Field(default=False, description="Refund if paid event")
    
    class Config:
        json_schema_extra = {
            "example": {
                "cancellation_reason": "Unexpected facility maintenance required",
                "cancelled_by": "Event Manager",
                "notify_participants": True,
                "refund_applicable": False
            }
        }


# Reschedule Event Schema
class RescheduleEvent(BaseModel):
    """Schema for rescheduling event"""
    new_date: str = Field(..., description="New date (YYYY-MM-DD)")
    new_start_time: str = Field(..., pattern="^([01][0-9]|2[0-3]):[0-5][0-9]$")
    new_end_time: str = Field(..., pattern="^([01][0-9]|2[0-3]):[0-5][0-9]$")
    reschedule_reason: str = Field(..., min_length=10, description="Reason for rescheduling")
    notify_participants: bool = Field(default=True, description="Notify participants")
    
    @field_validator('new_date')
    @classmethod
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
    
    class Config:
        json_schema_extra = {
            "example": {
                "new_date": "2024-02-22",
                "new_start_time": "14:00",
                "new_end_time": "16:00",
                "reschedule_reason": "Conflict with emergency drill",
                "notify_participants": True
            }
        }


# Statistics Schema
class EventStats(BaseModel):
    """Event statistics"""
    total_events: int
    upcoming_events: int
    ongoing_events: int
    completed_events: int
    cancelled_events: int
    events_by_type: Dict[str, int]
    events_by_status: Dict[str, int]
    events_this_week: int
    events_this_month: int
    total_participants: int
    average_attendance_rate: Optional[float] = Field(None, description="Average attendance percentage")
    most_popular_event_type: Optional[str] = None
    busiest_day: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_events": 150,
                "upcoming_events": 25,
                "ongoing_events": 2,
                "completed_events": 100,
                "cancelled_events": 5,
                "events_by_type": {
                    "meeting": 50,
                    "training": 30,
                    "seminar": 20,
                    "conference": 15
                },
                "events_by_status": {
                    "scheduled": 25,
                    "ongoing": 2,
                    "completed": 100,
                    "cancelled": 5
                },
                "events_this_week": 5,
                "events_this_month": 20,
                "total_participants": 3500,
                "average_attendance_rate": 85.5,
                "most_popular_event_type": "training",
                "busiest_day": "Wednesday"
            }
        }


# Calendar View Schema
class EventCalendarDay(BaseModel):
    """Single day in calendar"""
    date: str = Field(..., description="Date (YYYY-MM-DD)")
    events: List[EventResponse] = Field(default=[], description="Events on this day")
    event_count: int = Field(default=0, description="Number of events")
    has_events: bool = Field(default=False, description="Whether day has events")


class EventCalendar(BaseModel):
    """Calendar view of events"""
    month: str = Field(..., description="Month (YYYY-MM)")
    year: int
    month_number: int
    days: List[EventCalendarDay] = Field(..., description="Days with events")
    total_events: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "month": "2024-02",
                "year": 2024,
                "month_number": 2,
                "total_events": 15,
                "days": []
            }
        }


# Export Schema
class EventExport(BaseModel):
    """Export events"""
    filters: EventFilter = Field(..., description="Filters to apply")
    export_format: str = Field(..., pattern="^(csv|xlsx|pdf|ical)$", description="Export format")
    include_participants: bool = Field(default=False)
    include_agenda: bool = Field(default=False)
    filename: Optional[str] = None


# Bulk Operations
class EventBulkStatusUpdate(BaseModel):
    """Bulk update event status"""
    event_ids: List[int] = Field(..., min_length=1, max_length=50)
    status: EventStatus
    notes: Optional[str] = None
    
    @field_validator('event_ids')
    @classmethod
    def validate_ids(cls, v):
        if len(v) > 50:
            raise ValueError("Cannot update more than 50 events at once")
        return v