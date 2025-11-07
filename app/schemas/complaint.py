"""
Complaint Schemas
Pydantic schemas for patient and staff complaints/grievances management
"""

from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict, EmailStr
from typing import Optional, Any, List, Dict, Union
from datetime import datetime, date, timedelta
from enum import Enum
import json
import re


# Enums
class ComplainantType(str, Enum):
    """Valid complainant types"""
    PATIENT = "patient"
    VISITOR = "visitor"
    STAFF = "staff"
    DOCTOR = "doctor"
    NURSE = "nurse"
    VENDOR = "vendor"
    FAMILY = "family"
    GUARDIAN = "guardian"
    OTHER = "other"


class ComplaintCategory(str, Enum):
    """Valid complaint categories"""
    MEDICAL_CARE = "medical_care"
    STAFF_BEHAVIOR = "staff_behavior"
    FACILITY = "facility"
    BILLING = "billing"
    ADMINISTRATION = "administration"
    HYGIENE = "hygiene"
    FOOD = "food"
    WAITING_TIME = "waiting_time"
    COMMUNICATION = "communication"
    PRIVACY = "privacy"
    SAFETY = "safety"
    EQUIPMENT = "equipment"
    PHARMACY = "pharmacy"
    LABORATORY = "laboratory"
    RADIOLOGY = "radiology"


class ComplaintSeverity(str, Enum):
    """Valid severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ComplaintStatus(str, Enum):
    """Valid complaint statuses"""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    REJECTED = "rejected"
    PENDING_REVIEW = "pending_review"
    ESCALATED = "escalated"


class SatisfactionRating(int, Enum):
    """Satisfaction rating values"""
    VERY_DISSATISFIED = 1
    DISSATISFIED = 2
    NEUTRAL = 3
    SATISFIED = 4
    VERY_SATISFIED = 5


# Helper Schemas
class Attachment(BaseModel):
    """Attachment file information"""
    url: str = Field(..., max_length=500, description="Attachment URL")
    filename: str = Field(..., max_length=200, description="Original filename")
    file_type: str = Field(..., max_length=50, description="MIME type")
    file_size: Optional[int] = Field(None, ge=0, description="File size in bytes")
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    uploaded_by: Optional[str] = Field(None, description="User who uploaded")
    
    @field_validator('file_size')
    @classmethod
    def validate_file_size(cls, v):
        """Validate file size (max 10MB)"""
        if v and v > 10 * 1024 * 1024:
            raise ValueError("File size cannot exceed 10MB")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://cdn.example.com/complaints/evidence123.jpg",
                "filename": "evidence_photo.jpg",
                "file_type": "image/jpeg",
                "file_size": 524288,
                "uploaded_at": "2024-01-15T10:30:00",
                "uploaded_by": "John Doe"
            }
        }


class ComplainantInfo(BaseModel):
    """Complainant contact information"""
    name: str = Field(..., min_length=1, max_length=200, description="Complainant name")
    email: Optional[EmailStr] = Field(None, description="Email address")
    phone: str = Field(..., max_length=20, description="Phone number")
    type: ComplainantType = Field(..., description="Type of complainant")
    address: Optional[str] = Field(None, max_length=500, description="Address")
    relationship: Optional[str] = Field(None, max_length=100, description="Relationship to patient (if applicable)")
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        """Validate phone number format"""
        cleaned = re.sub(r'[\s\-\(\)]', '', v)
        if not re.match(r'^\+?[0-9]{10,15}$', cleaned):
            raise ValueError("Invalid phone number format")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+1-555-123-4567",
                "type": "patient",
                "address": "123 Main St, New York, NY 10001",
                "relationship": "Self"
            }
        }


class AssignmentInfo(BaseModel):
    """Assignment information"""
    assigned_to: str = Field(..., description="Person/department assigned to")
    assigned_by: Optional[str] = Field(None, description="Person who assigned")
    assigned_date: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = Field(None, description="Assignment notes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "assigned_to": "Patient Relations Manager",
                "assigned_by": "Admin",
                "assigned_date": "2024-01-15T10:30:00",
                "notes": "High priority - requires immediate attention"
            }
        }


class ResolutionInfo(BaseModel):
    """Resolution information"""
    resolution: str = Field(..., min_length=10, description="Resolution description")
    resolved_by: str = Field(..., description="Person who resolved")
    resolved_date: datetime = Field(default_factory=datetime.utcnow)
    resolution_time_hours: Optional[int] = Field(None, ge=0, description="Time taken to resolve")
    actions_taken: Optional[List[str]] = Field(None, description="Actions taken to resolve")
    preventive_measures: Optional[str] = Field(None, description="Preventive measures implemented")
    
    class Config:
        json_schema_extra = {
            "example": {
                "resolution": "Issue was addressed with staff member. Apology issued to patient. Additional training scheduled.",
                "resolved_by": "Dr. Jane Smith",
                "resolved_date": "2024-01-16T14:30:00",
                "resolution_time_hours": 28,
                "actions_taken": [
                    "Staff counseling",
                    "Patient apology",
                    "Process improvement"
                ],
                "preventive_measures": "Updated staff training protocol on patient communication"
            }
        }


class FollowUpInfo(BaseModel):
    """Follow-up information"""
    followup_date: str = Field(..., description="Follow-up date (YYYY-MM-DD)")
    followup_notes: Optional[str] = Field(None, description="Follow-up notes")
    followup_by: Optional[str] = Field(None, description="Person responsible for follow-up")
    followup_status: Optional[str] = Field(None, description="Follow-up status")
    completed_date: Optional[datetime] = Field(None, description="When follow-up was completed")
    
    @field_validator('followup_date')
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
                "followup_date": "2024-01-30",
                "followup_notes": "Check patient satisfaction after resolution",
                "followup_by": "Patient Relations Team",
                "followup_status": "Scheduled"
            }
        }


class SatisfactionFeedback(BaseModel):
    """Satisfaction feedback"""
    is_satisfied: bool = Field(..., description="Whether complainant is satisfied")
    rating: SatisfactionRating = Field(..., description="Satisfaction rating (1-5)")
    comments: Optional[str] = Field(None, max_length=1000, description="Additional comments")
    feedback_date: datetime = Field(default_factory=datetime.utcnow)
    would_recommend: Optional[bool] = Field(None, description="Would recommend the hospital")
    
    class Config:
        json_schema_extra = {
            "example": {
                "is_satisfied": True,
                "rating": 4,
                "comments": "Issue was resolved promptly and professionally",
                "feedback_date": "2024-01-17T10:00:00",
                "would_recommend": True
            }
        }


# Nested Schemas for Relationships
class PatientBasic(BaseModel):
    """Basic patient info"""
    id: int
    full_name: str
    patient_number: Optional[str] = None
    phone: Optional[str] = None
    
    class Config:
        from_attributes = True


class DepartmentBasic(BaseModel):
    """Basic department info"""
    id: int
    name: str
    head_name: Optional[str] = None
    
    class Config:
        from_attributes = True


# Base Schema
class ComplaintBase(BaseModel):
    """Base schema for complaints"""
    complaint_number: str = Field(..., max_length=20, description="Unique complaint number")
    title: str = Field(..., min_length=5, max_length=200, description="Complaint title/subject")
    description: str = Field(..., min_length=10, description="Detailed description")
    
    # Complainant
    complainant_name: str = Field(..., max_length=200, description="Complainant name")
    complainant_email: Optional[EmailStr] = Field(None, description="Email address")
    complainant_phone: str = Field(..., max_length=20, description="Phone number")
    complainant_type: ComplainantType = Field(..., description="Type of complainant")
    
    # References
    patient_id: Optional[int] = Field(None, description="Patient ID if applicable")
    department_id: Optional[int] = Field(None, description="Department ID")
    
    # Classification
    category: ComplaintCategory = Field(..., description="Complaint category")
    severity: ComplaintSeverity = Field(default=ComplaintSeverity.MEDIUM, description="Severity level")
    status: ComplaintStatus = Field(default=ComplaintStatus.OPEN, description="Current status")
    
    # Dates
    incident_date: Optional[str] = Field(None, description="Date of incident (YYYY-MM-DD)")
    filed_date: str = Field(..., description="Date complaint was filed (YYYY-MM-DD)")
    
    # Assignment
    assigned_to: Optional[str] = Field(None, max_length=200, description="Assigned to")
    assigned_date: Optional[str] = Field(None, description="Assignment date")
    
    # Resolution
    resolution: Optional[str] = Field(None, description="Resolution description")
    resolved_by: Optional[str] = Field(None, max_length=200, description="Resolved by")
    resolved_date: Optional[str] = Field(None, description="Resolution date")
    resolution_time_hours: Optional[int] = Field(None, ge=0, description="Resolution time")
    
    # Follow-up
    requires_followup: bool = Field(default=False, description="Requires follow-up")
    followup_date: Optional[str] = Field(None, description="Follow-up date")
    followup_notes: Optional[str] = Field(None, description="Follow-up notes")
    
    # Satisfaction
    is_satisfied: Optional[bool] = Field(None, description="Satisfaction status")
    satisfaction_rating: Optional[int] = Field(None, ge=1, le=5, description="Rating 1-5")
    satisfaction_comments: Optional[str] = Field(None, description="Satisfaction comments")
    
    # Attachments
    attachments: Optional[List[str]] = Field(None, description="Attachment URLs")
    
    # Notes
    notes: Optional[str] = Field(None, description="Public notes")
    internal_notes: Optional[str] = Field(None, description="Internal/staff notes")

    @field_validator('complainant_phone')
    @classmethod
    def validate_phone(cls, v):
        """Validate phone number"""
        cleaned = re.sub(r'[\s\-\(\)]', '', v)
        if not re.match(r'^\+?[0-9]{10,15}$', cleaned):
            raise ValueError("Invalid phone number format")
        return v
    
    @field_validator('incident_date', 'filed_date', 'assigned_date', 'resolved_date', 'followup_date')
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
    
    @field_validator('attachments', mode='before')
    @classmethod
    def parse_attachments(cls, v):
        """Parse attachments if JSON string"""
        if v is None:
            return None
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                raise ValueError("Attachments must be valid JSON array")
        return v
    
    @model_validator(mode='after')
    def validate_resolution_fields(self):
        """Validate resolution-related fields consistency"""
        if self.status in [ComplaintStatus.RESOLVED, ComplaintStatus.CLOSED]:
            if not self.resolution:
                raise ValueError("Resolution is required when status is resolved or closed")
            if not self.resolved_date:
                raise ValueError("Resolved date is required when status is resolved or closed")
        return self
    
    @model_validator(mode='after')
    def validate_followup_fields(self):
        """Validate follow-up fields consistency"""
        if self.requires_followup and not self.followup_date:
            raise ValueError("Follow-up date is required when follow-up is needed")
        return self
    
    @model_validator(mode='after')
    def validate_dates_chronology(self):
        """Validate chronological order of dates"""
        dates = []
        
        if self.incident_date:
            dates.append(('incident', datetime.strptime(self.incident_date, '%Y-%m-%d')))
        if self.filed_date:
            dates.append(('filed', datetime.strptime(self.filed_date, '%Y-%m-%d')))
        if self.assigned_date:
            dates.append(('assigned', datetime.strptime(self.assigned_date, '%Y-%m-%d')))
        if self.resolved_date:
            dates.append(('resolved', datetime.strptime(self.resolved_date, '%Y-%m-%d')))
        
        # Incident should be before filed
        if self.incident_date and self.filed_date:
            incident = datetime.strptime(self.incident_date, '%Y-%m-%d')
            filed = datetime.strptime(self.filed_date, '%Y-%m-%d')
            if incident > filed:
                raise ValueError("Incident date cannot be after filed date")
        
        return self


# Create Schema
class ComplaintCreate(BaseModel):
    """Schema for creating new complaint"""
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=10)
    
    # Complainant (use nested schema)
    complainant: ComplainantInfo = Field(..., description="Complainant information")
    
    # References
    patient_id: Optional[int] = None
    department_id: Optional[int] = None
    
    # Classification
    category: ComplaintCategory
    severity: ComplaintSeverity = Field(default=ComplaintSeverity.MEDIUM)
    
    # Dates
    incident_date: Optional[str] = None
    filed_date: Optional[str] = Field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d'))
    
    # Attachments
    attachments: Optional[List[Attachment]] = Field(None, max_length=10, description="Evidence attachments")
    
    # Notes
    notes: Optional[str] = None
    
    # Auto-generate complaint number
    complaint_number: Optional[str] = Field(None, description="Auto-generated if not provided")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Long wait time in emergency",
                "description": "Waited over 3 hours in emergency room despite severe pain",
                "complainant": {
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "phone": "+1-555-123-4567",
                    "type": "patient"
                },
                "patient_id": 123,
                "category": "waiting_time",
                "severity": "high",
                "incident_date": "2024-01-14",
                "filed_date": "2024-01-15",
                "notes": "Patient was in significant discomfort"
            }
        }


# Update Schema
class ComplaintUpdate(BaseModel):
    """Schema for updating complaint"""
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    description: Optional[str] = Field(None, min_length=10)
    category: Optional[ComplaintCategory] = None
    severity: Optional[ComplaintSeverity] = None
    status: Optional[ComplaintStatus] = None
    department_id: Optional[int] = None
    assigned_to: Optional[str] = Field(None, max_length=200)
    assigned_date: Optional[str] = None
    resolution: Optional[str] = None
    resolved_by: Optional[str] = Field(None, max_length=200)
    resolved_date: Optional[str] = None
    requires_followup: Optional[bool] = None
    followup_date: Optional[str] = None
    followup_notes: Optional[str] = None
    notes: Optional[str] = None
    internal_notes: Optional[str] = None
    
    @field_validator('assigned_date', 'resolved_date', 'followup_date')
    @classmethod
    def validate_date(cls, v):
        if v is None:
            return None
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")


# Response Schema
class ComplaintResponse(ComplaintBase):
    """Schema for complaint response"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    # Calculated fields
    days_open: Optional[int] = Field(None, description="Days since filed")
    is_overdue: bool = Field(default=False, description="Whether complaint is overdue")
    sla_deadline: Optional[datetime] = Field(None, description="SLA deadline")
    
    model_config = ConfigDict(from_attributes=True)
    
    @model_validator(mode='after')
    def calculate_days_open(self):
        """Calculate days since complaint was filed"""
        if self.filed_date:
            filed = datetime.strptime(self.filed_date, '%Y-%m-%d')
            if self.status in [ComplaintStatus.RESOLVED, ComplaintStatus.CLOSED]:
                if self.resolved_date:
                    resolved = datetime.strptime(self.resolved_date, '%Y-%m-%d')
                    self.days_open = (resolved - filed).days
            else:
                self.days_open = (datetime.now() - filed).days
        
        # Calculate SLA deadline based on severity
        if self.filed_date and self.status not in [ComplaintStatus.RESOLVED, ComplaintStatus.CLOSED]:
            filed = datetime.strptime(self.filed_date, '%Y-%m-%d')
            sla_days = {
                ComplaintSeverity.CRITICAL: 1,
                ComplaintSeverity.HIGH: 3,
                ComplaintSeverity.MEDIUM: 7,
                ComplaintSeverity.LOW: 14
            }
            deadline_days = sla_days.get(self.severity, 7)
            self.sla_deadline = filed + timedelta(days=deadline_days)
            self.is_overdue = datetime.now() > self.sla_deadline
        
        return self
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "complaint_number": "CMP-2024-0001",
                "title": "Long wait time in emergency",
                "description": "Waited over 3 hours in emergency room",
                "complainant_name": "John Doe",
                "complainant_type": "patient",
                "category": "waiting_time",
                "severity": "high",
                "status": "in_progress",
                "filed_date": "2024-01-15",
                "days_open": 2,
                "is_overdue": False,
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00"
            }
        }


# Detailed Response with Relationships
class ComplaintDetailResponse(ComplaintResponse):
    """Detailed complaint with relationships"""
    patient: Optional[PatientBasic] = None
    department: Optional[DepartmentBasic] = None
    attachment_details: Optional[List[Attachment]] = None
    history: Optional[List[Dict[str, Any]]] = Field(None, description="Status change history")
    
    model_config = ConfigDict(from_attributes=True)


# List Response Schema
class ComplaintListResponse(BaseModel):
    """Schema for paginated list of complaints"""
    total: int = Field(..., description="Total number of records")
    page: int = Field(..., ge=1, description="Current page number")
    page_size: int = Field(..., ge=1, le=100, description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")
    items: List[ComplaintResponse] = Field(..., description="Complaint items")
    summary: Optional[Dict[str, Any]] = Field(None, description="Summary statistics")


# Filter Schema
class ComplaintFilter(BaseModel):
    """Schema for filtering complaints"""
    # String filters
    complaint_number: Optional[str] = Field(None, description="Filter by complaint number")
    title: Optional[str] = Field(None, description="Search in title")
    complainant_name: Optional[str] = Field(None, description="Search complainant name")
    
    # Type filters
    complainant_type: Optional[ComplainantType] = Field(None, description="Filter by complainant type")
    category: Optional[Union[ComplaintCategory, List[ComplaintCategory]]] = Field(None, description="Filter by category")
    severity: Optional[Union[ComplaintSeverity, List[ComplaintSeverity]]] = Field(None, description="Filter by severity")
    status: Optional[Union[ComplaintStatus, List[ComplaintStatus]]] = Field(None, description="Filter by status")
    
    # Reference filters
    patient_id: Optional[int] = Field(None, description="Filter by patient ID")
    department_id: Optional[int] = Field(None, description="Filter by department ID")
    
    # Assignment filters
    assigned_to: Optional[str] = Field(None, description="Filter by assignee")
    unassigned: Optional[bool] = Field(None, description="Show only unassigned")
    
    # Date filters
    filed_date_from: Optional[str] = Field(None, description="Filed from date")
    filed_date_to: Optional[str] = Field(None, description="Filed to date")
    incident_date_from: Optional[str] = Field(None, description="Incident from date")
    incident_date_to: Optional[str] = Field(None, description="Incident to date")
    
    # Status filters
    is_overdue: Optional[bool] = Field(None, description="Show overdue complaints")
    requires_followup: Optional[bool] = Field(None, description="Show requiring follow-up")
    is_satisfied: Optional[bool] = Field(None, description="Filter by satisfaction")
    
    # Satisfaction filter
    satisfaction_rating: Optional[int] = Field(None, ge=1, le=5, description="Filter by rating")
    
    # Search
    search: Optional[str] = Field(None, description="Search in title, description")
    
    # Pagination
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")
    
    # Sorting
    sort_by: Optional[str] = Field("filed_date", description="Field to sort by")
    sort_order: Optional[str] = Field("desc", pattern="^(asc|desc)$", description="Sort order")
    
    # Include relationships
    include_patient: bool = Field(False, description="Include patient details")
    include_department: bool = Field(False, description="Include department details")
    include_history: bool = Field(False, description="Include status history")

    @field_validator('filed_date_from', 'filed_date_to', 'incident_date_from', 'incident_date_to')
    @classmethod
    def validate_date(cls, v):
        if v is None:
            return None
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")


# Assignment Schema
class AssignComplaint(BaseModel):
    """Schema for assigning complaint"""
    assigned_to: str = Field(..., max_length=200, description="Person/department to assign to")
    assigned_by: Optional[str] = Field(None, description="Person assigning")
    notes: Optional[str] = Field(None, description="Assignment notes")
    priority: Optional[str] = Field(None, pattern="^(low|normal|high|urgent)$")
    due_date: Optional[str] = Field(None, description="Expected resolution date")
    
    @field_validator('due_date')
    @classmethod
    def validate_date(cls, v):
        if v is None:
            return None
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
    
    class Config:
        json_schema_extra = {
            "example": {
                "assigned_to": "Patient Relations Manager",
                "assigned_by": "Admin",
                "notes": "Requires immediate attention",
                "priority": "high",
                "due_date": "2024-01-17"
            }
        }


# Resolution Schema
class ResolveComplaint(BaseModel):
    """Schema for resolving complaint"""
    resolution: str = Field(..., min_length=10, description="Resolution description")
    resolved_by: str = Field(..., description="Person resolving")
    resolved_date: Optional[str] = Field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d'))
    actions_taken: Optional[List[str]] = Field(None, description="Actions taken")
    preventive_measures: Optional[str] = Field(None, description="Preventive measures")
    requires_followup: bool = Field(default=False, description="Requires follow-up")
    followup_date: Optional[str] = Field(None, description="Follow-up date if needed")
    
    @field_validator('resolved_date', 'followup_date')
    @classmethod
    def validate_date(cls, v):
        if v is None:
            return None
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
    
    @model_validator(mode='after')
    def validate_followup_date(self):
        if self.requires_followup and not self.followup_date:
            raise ValueError("Follow-up date required when follow-up is needed")
        return self
    
    class Config:
        json_schema_extra = {
            "example": {
                "resolution": "Staff counseling completed. Patient contacted and apology issued. Process improvements implemented.",
                "resolved_by": "Dr. Jane Smith",
                "resolved_date": "2024-01-16",
                "actions_taken": [
                    "Staff training on patient communication",
                    "Personal apology to patient",
                    "Updated triage protocol"
                ],
                "preventive_measures": "Implemented new patient communication guidelines",
                "requires_followup": True,
                "followup_date": "2024-01-30"
            }
        }


# Close Complaint Schema
class CloseComplaint(BaseModel):
    """Schema for closing complaint"""
    closure_notes: str = Field(..., min_length=10, description="Closure notes")
    closed_by: str = Field(..., description="Person closing")
    reason: Optional[str] = Field(None, description="Reason for closure")
    
    class Config:
        json_schema_extra = {
            "example": {
                "closure_notes": "Patient satisfied with resolution. No further action required.",
                "closed_by": "Patient Relations Manager",
                "reason": "Resolved to satisfaction"
            }
        }


# Escalate Complaint Schema
class EscalateComplaint(BaseModel):
    """Schema for escalating complaint"""
    escalate_to: str = Field(..., description="Escalate to (person/department)")
    escalation_reason: str = Field(..., min_length=10, description="Reason for escalation")
    escalated_by: str = Field(..., description="Person escalating")
    priority: str = Field(default="high", pattern="^(high|critical)$")
    notes: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "escalate_to": "Chief Medical Officer",
                "escalation_reason": "Involves potential patient safety issue requiring senior review",
                "escalated_by": "Patient Relations Manager",
                "priority": "critical",
                "notes": "Requires immediate attention"
            }
        }


# Reject Complaint Schema
class RejectComplaint(BaseModel):
    """Schema for rejecting complaint"""
    rejection_reason: str = Field(..., min_length=10, description="Reason for rejection")
    rejected_by: str = Field(..., description="Person rejecting")
    alternative_action: Optional[str] = Field(None, description="Alternative action suggested")
    
    class Config:
        json_schema_extra = {
            "example": {
                "rejection_reason": "Complaint does not fall under hospital jurisdiction - related to external insurance provider",
                "rejected_by": "Compliance Officer",
                "alternative_action": "Referred to insurance company directly"
            }
        }


# Add Follow-up Schema
class AddFollowUp(BaseModel):
    """Schema for adding follow-up"""
    followup_date: str = Field(..., description="Follow-up date")
    followup_notes: str = Field(..., min_length=5, description="Follow-up notes")
    followup_by: str = Field(..., description="Person responsible")
    reminder_date: Optional[str] = Field(None, description="Reminder date")
    
    @field_validator('followup_date', 'reminder_date')
    @classmethod
    def validate_date(cls, v):
        if v is None:
            return None
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")


# Record Satisfaction Schema
class RecordSatisfaction(BaseModel):
    """Schema for recording satisfaction feedback"""
    is_satisfied: bool = Field(..., description="Satisfaction status")
    rating: SatisfactionRating = Field(..., description="Rating 1-5")
    comments: Optional[str] = Field(None, max_length=1000)
    would_recommend: Optional[bool] = Field(None, description="Would recommend hospital")
    feedback_method: Optional[str] = Field(None, description="How feedback was collected")
    
    class Config:
        json_schema_extra = {
            "example": {
                "is_satisfied": True,
                "rating": 4,
                "comments": "Issue resolved quickly and professionally",
                "would_recommend": True,
                "feedback_method": "Phone survey"
            }
        }


# Statistics Schema
class ComplaintStats(BaseModel):
    """Complaint statistics"""
    total_complaints: int
    open_complaints: int
    in_progress_complaints: int
    resolved_complaints: int
    closed_complaints: int
    rejected_complaints: int
    
    # By category
    complaints_by_category: Dict[str, int]
    complaints_by_severity: Dict[str, int]
    complaints_by_complainant_type: Dict[str, int]
    
    # By department
    complaints_by_department: Dict[str, int]
    
    # Time-based
    complaints_today: int
    complaints_this_week: int
    complaints_this_month: int
    
    # SLA metrics
    overdue_complaints: int
    within_sla: int
    sla_compliance_rate: float = Field(..., description="Percentage within SLA")
    
    # Resolution metrics
    average_resolution_time_hours: Optional[float] = None
    median_resolution_time_hours: Optional[float] = None
    
    # Satisfaction metrics
    satisfaction_rate: Optional[float] = Field(None, description="Percentage satisfied")
    average_satisfaction_rating: Optional[float] = Field(None, description="Average rating")
    
    # Trends
    trend_last_30_days: Optional[List[Dict[str, Any]]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_complaints": 500,
                "open_complaints": 50,
                "in_progress_complaints": 80,
                "resolved_complaints": 320,
                "closed_complaints": 300,
                "rejected_complaints": 20,
                "complaints_by_category": {
                    "medical_care": 150,
                    "staff_behavior": 100,
                    "waiting_time": 80,
                    "facility": 70,
                    "billing": 60
                },
                "complaints_by_severity": {
                    "critical": 20,
                    "high": 80,
                    "medium": 250,
                    "low": 150
                },
                "complaints_by_complainant_type": {
                    "patient": 350,
                    "visitor": 80,
                    "staff": 40,
                    "family": 30
                },
                "complaints_by_department": {
                    "Emergency": 100,
                    "Inpatient": 80,
                    "Outpatient": 60
                },
                "complaints_today": 5,
                "complaints_this_week": 25,
                "complaints_this_month": 100,
                "overdue_complaints": 15,
                "within_sla": 35,
                "sla_compliance_rate": 85.0,
                "average_resolution_time_hours": 48.5,
                "median_resolution_time_hours": 36.0,
                "satisfaction_rate": 78.5,
                "average_satisfaction_rating": 3.8
            }
        }


# Dashboard Schema
class ComplaintDashboard(BaseModel):
    """Dashboard summary"""
    total_active: int
    new_today: int
    due_today: int
    overdue: int
    critical_severity: int
    pending_assignment: int
    pending_followup: int
    recent_complaints: List[ComplaintResponse]
    urgent_complaints: List[ComplaintResponse]
    satisfaction_summary: Dict[str, Any]
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_active": 130,
                "new_today": 5,
                "due_today": 8,
                "overdue": 12,
                "critical_severity": 3,
                "pending_assignment": 10,
                "pending_followup": 15,
                "recent_complaints": [],
                "urgent_complaints": [],
                "satisfaction_summary": {
                    "total_feedback": 250,
                    "satisfied": 195,
                    "satisfaction_rate": 78.0
                }
            }
        }


# Report Schema
class ComplaintReport(BaseModel):
    """Complaint report"""
    report_id: str
    report_type: str = Field(..., description="Type of report")
    period_start: datetime
    period_end: datetime
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    generated_by: Optional[str] = None
    
    # Summary
    summary: ComplaintStats
    
    # Details
    top_categories: List[Dict[str, Any]]
    top_departments: List[Dict[str, Any]]
    resolution_trends: List[Dict[str, Any]]
    satisfaction_trends: List[Dict[str, Any]]
    
    # Insights
    insights: List[str] = Field(default=[], description="Key insights")
    recommendations: List[str] = Field(default=[], description="Recommendations")
    
    class Config:
        json_schema_extra = {
            "example": {
                "report_id": "RPT-2024-01",
                "report_type": "monthly",
                "period_start": "2024-01-01T00:00:00",
                "period_end": "2024-01-31T23:59:59",
                "generated_at": "2024-02-01T09:00:00",
                "generated_by": "System",
                "insights": [
                    "Waiting time complaints increased by 15%",
                    "Emergency department has highest complaint volume"
                ],
                "recommendations": [
                    "Review emergency department staffing",
                    "Implement real-time wait time notifications"
                ]
            }
        }


# Export Schema
class ComplaintExport(BaseModel):
    """Export complaints"""
    filters: ComplaintFilter = Field(..., description="Filters to apply")
    export_format: str = Field(..., pattern="^(csv|xlsx|pdf|json)$")
    include_attachments: bool = Field(default=False)
    include_history: bool = Field(default=False)
    filename: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "filters": {
                    "status": "resolved",
                    "filed_date_from": "2024-01-01",
                    "filed_date_to": "2024-01-31"
                },
                "export_format": "xlsx",
                "include_attachments": False,
                "include_history": True,
                "filename": "complaints_january_2024.xlsx"
            }
        }


# Bulk Operations
class ComplaintBulkAssign(BaseModel):
    """Bulk assign complaints"""
    complaint_ids: List[int] = Field(..., min_length=1, max_length=50)
    assigned_to: str = Field(..., description="Assign to")
    notes: Optional[str] = None
    
    @field_validator('complaint_ids')
    @classmethod
    def validate_ids(cls, v):
        if len(v) > 50:
            raise ValueError("Cannot assign more than 50 complaints at once")
        return v


class ComplaintBulkStatusUpdate(BaseModel):
    """Bulk update status"""
    complaint_ids: List[int] = Field(..., min_length=1, max_length=50)
    status: ComplaintStatus = Field(..., description="New status")
    notes: Optional[str] = None


# Trend Analysis Schema
class ComplaintTrend(BaseModel):
    """Complaint trend data"""
    period: str = Field(..., description="Time period (day, week, month)")
    count: int = Field(..., description="Number of complaints")
    change_percentage: Optional[float] = Field(None, description="Change from previous period")
    
    class Config:
        json_schema_extra = {
            "example": {
                "period": "2024-01",
                "count": 45,
                "change_percentage": 12.5
            }
        }


class ComplaintTrendAnalysis(BaseModel):
    """Trend analysis response"""
    metric: str = Field(..., description="Metric being analyzed")
    time_range: str = Field(..., description="Time range")
    trends: List[ComplaintTrend]
    overall_trend: str = Field(..., pattern="^(increasing|decreasing|stable)$")
    insights: List[str] = Field(default=[])