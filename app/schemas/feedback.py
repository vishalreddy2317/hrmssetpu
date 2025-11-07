"""
Feedback Schemas
Pydantic schemas for patient and service feedback management
"""

from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict, EmailStr
from typing import Optional, List, Dict, Any, Union
from datetime import datetime, date
from enum import Enum
import json
import re


# Enums
class ServiceType(str, Enum):
    """Service types for feedback"""
    CONSULTATION = "consultation"
    ADMISSION = "admission"
    EMERGENCY = "emergency"
    LAB = "lab"
    PHARMACY = "pharmacy"
    OVERALL = "overall"
    SURGERY = "surgery"
    NURSING_CARE = "nursing_care"
    RADIOLOGY = "radiology"
    OUTPATIENT = "outpatient"
    INPATIENT = "inpatient"


class FeedbackStatus(str, Enum):
    """Feedback status"""
    RECEIVED = "received"
    REVIEWED = "reviewed"
    RESPONDED = "responded"
    ARCHIVED = "archived"
    PENDING_RESPONSE = "pending_response"


class FeedbackSource(str, Enum):
    """Feedback submission source"""
    WEBSITE = "website"
    APP = "app"
    EMAIL = "email"
    SURVEY = "survey"
    PHONE = "phone"
    SMS = "sms"
    IN_PERSON = "in_person"
    KIOSK = "kiosk"


class RatingCategory(str, Enum):
    """Rating categories"""
    OVERALL = "overall"
    STAFF_BEHAVIOR = "staff_behavior"
    CLEANLINESS = "cleanliness"
    FACILITIES = "facilities"
    WAITING_TIME = "waiting_time"
    TREATMENT_QUALITY = "treatment_quality"


# Helper Schemas
class PatientBasic(BaseModel):
    """Basic patient information"""
    id: int
    full_name: str
    patient_number: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    
    class Config:
        from_attributes = True


class DoctorBasic(BaseModel):
    """Basic doctor information"""
    id: int
    full_name: str
    specialization: Optional[str] = None
    department: Optional[str] = None
    
    class Config:
        from_attributes = True


class DepartmentBasic(BaseModel):
    """Basic department information"""
    id: int
    name: str
    head_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class RatingBreakdown(BaseModel):
    """Detailed rating breakdown"""
    overall_rating: int = Field(..., ge=1, le=5)
    staff_behavior_rating: Optional[int] = Field(None, ge=1, le=5)
    cleanliness_rating: Optional[int] = Field(None, ge=1, le=5)
    facilities_rating: Optional[int] = Field(None, ge=1, le=5)
    waiting_time_rating: Optional[int] = Field(None, ge=1, le=5)
    treatment_quality_rating: Optional[int] = Field(None, ge=1, le=5)
    average_rating: Optional[float] = Field(None, description="Average of all ratings")
    
    @model_validator(mode='after')
    def calculate_average(self):
        """Calculate average rating"""
        ratings = [
            self.overall_rating,
            self.staff_behavior_rating,
            self.cleanliness_rating,
            self.facilities_rating,
            self.waiting_time_rating,
            self.treatment_quality_rating
        ]
        valid_ratings = [r for r in ratings if r is not None]
        if valid_ratings:
            self.average_rating = round(sum(valid_ratings) / len(valid_ratings), 2)
        return self
    
    class Config:
        json_schema_extra = {
            "example": {
                "overall_rating": 4,
                "staff_behavior_rating": 5,
                "cleanliness_rating": 4,
                "facilities_rating": 4,
                "waiting_time_rating": 3,
                "treatment_quality_rating": 5,
                "average_rating": 4.17
            }
        }


class FeedbackComment(BaseModel):
    """Feedback comments"""
    positive_comments: Optional[str] = Field(None, description="What went well")
    negative_comments: Optional[str] = Field(None, description="Areas for improvement")
    suggestions: Optional[str] = Field(None, description="Suggestions for improvement")
    
    class Config:
        json_schema_extra = {
            "example": {
                "positive_comments": "The staff was very friendly and professional. The facility was clean and well-maintained.",
                "negative_comments": "The waiting time was longer than expected.",
                "suggestions": "Consider implementing an appointment reminder system to reduce wait times."
            }
        }


class FeedbackResponse(BaseModel):
    """Response to feedback"""
    response: str = Field(..., min_length=10, description="Response text")
    responded_by: str = Field(..., max_length=200, description="Person responding")
    response_date: Optional[str] = Field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d'))
    
    @field_validator('response_date')
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
                "response": "Thank you for your valuable feedback. We have noted your concern about waiting times and are implementing measures to improve our scheduling system.",
                "responded_by": "Patient Relations Manager",
                "response_date": "2024-01-16"
            }
        }


# Base Schema
class FeedbackBase(BaseModel):
    """Base schema for feedback"""
    feedback_number: str = Field(..., max_length=20, description="Unique feedback identifier")
    
    # Patient Info (optional - can be anonymous)
    patient_id: Optional[int] = Field(None, description="Patient ID if logged in")
    patient_name: Optional[str] = Field(None, max_length=200, description="Patient name")
    email: Optional[EmailStr] = Field(None, description="Contact email")
    phone: Optional[str] = Field(None, max_length=20, description="Contact phone")
    
    # Service Details
    service_type: ServiceType = Field(..., description="Type of service being reviewed")
    doctor_id: Optional[int] = Field(None, description="Doctor ID if applicable")
    department_id: Optional[int] = Field(None, description="Department ID")
    
    # Ratings (1-5 scale)
    overall_rating: int = Field(..., ge=1, le=5, description="Overall rating (1-5)")
    staff_behavior_rating: Optional[int] = Field(None, ge=1, le=5, description="Staff behavior rating")
    cleanliness_rating: Optional[int] = Field(None, ge=1, le=5, description="Cleanliness rating")
    facilities_rating: Optional[int] = Field(None, ge=1, le=5, description="Facilities rating")
    waiting_time_rating: Optional[int] = Field(None, ge=1, le=5, description="Waiting time rating")
    treatment_quality_rating: Optional[int] = Field(None, ge=1, le=5, description="Treatment quality rating")
    
    # Comments
    positive_comments: Optional[str] = Field(None, description="Positive feedback")
    negative_comments: Optional[str] = Field(None, description="Negative feedback")
    suggestions: Optional[str] = Field(None, description="Suggestions")
    
    # Recommendation
    would_recommend: Optional[bool] = Field(None, description="Would recommend hospital")
    
    # Dates
    feedback_date: str = Field(..., description="Feedback submission date (YYYY-MM-DD)")
    visit_date: Optional[str] = Field(None, description="Visit/service date (YYYY-MM-DD)")
    
    # Status
    status: FeedbackStatus = Field(default=FeedbackStatus.RECEIVED, description="Feedback status")
    
    # Response
    response: Optional[str] = Field(None, description="Response to feedback")
    responded_by: Optional[str] = Field(None, max_length=200, description="Person who responded")
    response_date: Optional[str] = Field(None, description="Response date")
    
    # Publication
    is_public: bool = Field(default=False, description="Display publicly")
    is_approved: bool = Field(default=False, description="Approved for publication")
    
    # Source
    source: FeedbackSource = Field(default=FeedbackSource.WEBSITE, description="Submission source")

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        """Validate phone number format"""
        if v is None:
            return None
        cleaned = re.sub(r'[\s\-\(\)]', '', v)
        if not re.match(r'^\+?[0-9]{10,15}$', cleaned):
            raise ValueError("Invalid phone number format")
        return v
    
    @field_validator('feedback_date', 'visit_date', 'response_date')
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
    
    @model_validator(mode='after')
    def validate_dates_chronology(self):
        """Validate date chronology"""
        if self.visit_date and self.feedback_date:
            visit = datetime.strptime(self.visit_date, '%Y-%m-%d')
            feedback = datetime.strptime(self.feedback_date, '%Y-%m-%d')
            if visit > feedback:
                raise ValueError("Visit date cannot be after feedback date")
        return self
    
    @model_validator(mode='after')
    def validate_contact_info(self):
        """Ensure at least some contact info for non-anonymous feedback"""
        if not self.patient_id and not self.email and not self.phone:
            # Anonymous feedback is allowed but warn
            pass
        return self


# Create Schema
class FeedbackCreate(BaseModel):
    """Schema for creating feedback"""
    # Patient info (optional for anonymous)
    patient_id: Optional[int] = None
    patient_name: Optional[str] = Field(None, max_length=200)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    
    # Service details
    service_type: ServiceType
    doctor_id: Optional[int] = None
    department_id: Optional[int] = None
    
    # Ratings (only overall is required)
    overall_rating: int = Field(..., ge=1, le=5)
    staff_behavior_rating: Optional[int] = Field(None, ge=1, le=5)
    cleanliness_rating: Optional[int] = Field(None, ge=1, le=5)
    facilities_rating: Optional[int] = Field(None, ge=1, le=5)
    waiting_time_rating: Optional[int] = Field(None, ge=1, le=5)
    treatment_quality_rating: Optional[int] = Field(None, ge=1, le=5)
    
    # Comments
    positive_comments: Optional[str] = None
    negative_comments: Optional[str] = None
    suggestions: Optional[str] = None
    
    # Recommendation
    would_recommend: Optional[bool] = None
    
    # Dates
    feedback_date: Optional[str] = Field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d'))
    visit_date: Optional[str] = None
    
    # Source
    source: FeedbackSource = Field(default=FeedbackSource.WEBSITE)
    
    # Anonymous option
    is_anonymous: bool = Field(default=False, description="Submit anonymously")
    
    # Auto-generated
    feedback_number: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "patient_name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+1-555-123-4567",
                "service_type": "consultation",
                "doctor_id": 45,
                "department_id": 5,
                "overall_rating": 5,
                "staff_behavior_rating": 5,
                "cleanliness_rating": 4,
                "facilities_rating": 4,
                "waiting_time_rating": 3,
                "treatment_quality_rating": 5,
                "positive_comments": "The doctor was very thorough and took time to explain everything. Staff was friendly.",
                "negative_comments": "Had to wait 30 minutes past appointment time.",
                "suggestions": "Better appointment scheduling to reduce wait times.",
                "would_recommend": True,
                "visit_date": "2024-01-15",
                "source": "website"
            }
        }


# Update Schema
class FeedbackUpdate(BaseModel):
    """Schema for updating feedback"""
    patient_name: Optional[str] = Field(None, max_length=200)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    overall_rating: Optional[int] = Field(None, ge=1, le=5)
    staff_behavior_rating: Optional[int] = Field(None, ge=1, le=5)
    cleanliness_rating: Optional[int] = Field(None, ge=1, le=5)
    facilities_rating: Optional[int] = Field(None, ge=1, le=5)
    waiting_time_rating: Optional[int] = Field(None, ge=1, le=5)
    treatment_quality_rating: Optional[int] = Field(None, ge=1, le=5)
    positive_comments: Optional[str] = None
    negative_comments: Optional[str] = None
    suggestions: Optional[str] = None
    would_recommend: Optional[bool] = None
    status: Optional[FeedbackStatus] = None
    is_public: Optional[bool] = None
    is_approved: Optional[bool] = None


# Response Schema
class FeedbackResponseSchema(FeedbackBase):
    """Schema for feedback response"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    # Calculated fields
    days_since_feedback: Optional[int] = Field(None, description="Days since submitted")
    days_since_visit: Optional[int] = Field(None, description="Days since visit")
    is_recent: bool = Field(default=False, description="Submitted within 7 days")
    is_positive: bool = Field(default=False, description="Rating >= 4")
    is_negative: bool = Field(default=False, description="Rating <= 2")
    has_response: bool = Field(default=False, description="Has been responded to")
    response_time_days: Optional[int] = Field(None, description="Days to respond")
    sentiment: Optional[str] = Field(None, description="positive, neutral, negative")
    
    model_config = ConfigDict(from_attributes=True)
    
    @model_validator(mode='after')
    def calculate_fields(self):
        """Calculate additional fields"""
        # Days since feedback
        if self.feedback_date:
            feedback_dt = datetime.strptime(self.feedback_date, '%Y-%m-%d')
            self.days_since_feedback = (datetime.now() - feedback_dt).days
            self.is_recent = self.days_since_feedback <= 7
        
        # Days since visit
        if self.visit_date:
            visit_dt = datetime.strptime(self.visit_date, '%Y-%m-%d')
            self.days_since_visit = (datetime.now() - visit_dt).days
        
        # Sentiment
        if self.overall_rating >= 4:
            self.sentiment = "positive"
            self.is_positive = True
        elif self.overall_rating <= 2:
            self.sentiment = "negative"
            self.is_negative = True
        else:
            self.sentiment = "neutral"
        
        # Response status
        self.has_response = self.response is not None
        
        # Response time
        if self.response_date and self.feedback_date:
            feedback_dt = datetime.strptime(self.feedback_date, '%Y-%m-%d')
            response_dt = datetime.strptime(self.response_date, '%Y-%m-%d')
            self.response_time_days = (response_dt - feedback_dt).days
        
        return self
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "feedback_number": "FB-2024-0001",
                "patient_name": "John Doe",
                "email": "john.doe@example.com",
                "service_type": "consultation",
                "overall_rating": 5,
                "staff_behavior_rating": 5,
                "cleanliness_rating": 4,
                "would_recommend": True,
                "feedback_date": "2024-01-15",
                "status": "responded",
                "is_positive": True,
                "sentiment": "positive",
                "has_response": True,
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-16T14:00:00"
            }
        }


# Detail Response with Relationships
class FeedbackDetailResponse(FeedbackResponseSchema):
    """Detailed feedback with relationships"""
    patient: Optional[PatientBasic] = None
    doctor: Optional[DoctorBasic] = None
    department: Optional[DepartmentBasic] = None
    
    # Enhanced details
    rating_breakdown: Optional[RatingBreakdown] = None
    
    model_config = ConfigDict(from_attributes=True)


# List Response Schema
class FeedbackListResponse(BaseModel):
    """Schema for paginated list of feedbacks"""
    total: int = Field(..., description="Total number of records")
    page: int = Field(..., ge=1, description="Current page number")
    page_size: int = Field(..., ge=1, le=100, description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")
    items: List[FeedbackResponseSchema] = Field(..., description="Feedback items")
    summary: Optional[Dict[str, Any]] = Field(None, description="Summary statistics")


# Filter Schema
class FeedbackFilter(BaseModel):
    """Schema for filtering feedback"""
    # ID filters
    patient_id: Optional[int] = Field(None, description="Filter by patient ID")
    doctor_id: Optional[int] = Field(None, description="Filter by doctor ID")
    department_id: Optional[int] = Field(None, description="Filter by department ID")
    
    # String filters
    feedback_number: Optional[str] = Field(None, description="Filter by feedback number")
    patient_name: Optional[str] = Field(None, description="Search patient name")
    email: Optional[str] = Field(None, description="Filter by email")
    
    # Type filters
    service_type: Optional[Union[ServiceType, List[ServiceType]]] = Field(None, description="Filter by service type")
    status: Optional[Union[FeedbackStatus, List[FeedbackStatus]]] = Field(None, description="Filter by status")
    source: Optional[FeedbackSource] = Field(None, description="Filter by source")
    
    # Rating filters
    overall_rating: Optional[int] = Field(None, ge=1, le=5, description="Filter by overall rating")
    min_rating: Optional[int] = Field(None, ge=1, le=5, description="Minimum rating")
    max_rating: Optional[int] = Field(None, ge=1, le=5, description="Maximum rating")
    
    # Boolean filters
    would_recommend: Optional[bool] = Field(None, description="Would recommend filter")
    is_public: Optional[bool] = Field(None, description="Public feedbacks only")
    is_approved: Optional[bool] = Field(None, description="Approved feedbacks only")
    has_response: Optional[bool] = Field(None, description="Has response")
    is_anonymous: Optional[bool] = Field(None, description="Anonymous feedbacks")
    
    # Sentiment filters
    positive_only: Optional[bool] = Field(None, description="Rating >= 4")
    negative_only: Optional[bool] = Field(None, description="Rating <= 2")
    
    # Date filters
    feedback_date_from: Optional[str] = Field(None, description="From date")
    feedback_date_to: Optional[str] = Field(None, description="To date")
    visit_date_from: Optional[str] = Field(None, description="Visit from date")
    visit_date_to: Optional[str] = Field(None, description="Visit to date")
    
    # Special filters
    recent_only: Optional[bool] = Field(None, description="Last 7 days only")
    pending_response: Optional[bool] = Field(None, description="Awaiting response")
    
    # Search
    search: Optional[str] = Field(None, description="Search in comments and suggestions")
    
    # Pagination
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")
    
    # Sorting
    sort_by: str = Field("feedback_date", description="Field to sort by")
    sort_order: str = Field("desc", pattern="^(asc|desc)$", description="Sort order")
    
    # Include relationships
    include_patient: bool = Field(False, description="Include patient details")
    include_doctor: bool = Field(False, description="Include doctor details")
    include_department: bool = Field(False, description="Include department details")

    @field_validator('feedback_date_from', 'feedback_date_to', 'visit_date_from', 'visit_date_to')
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
    def validate_rating_range(self):
        """Validate rating range"""
        if self.min_rating and self.max_rating:
            if self.min_rating > self.max_rating:
                raise ValueError("min_rating must be <= max_rating")
        return self


# Respond to Feedback Schema
class RespondToFeedback(BaseModel):
    """Schema for responding to feedback"""
    response: str = Field(..., min_length=10, max_length=2000, description="Response text")
    responded_by: str = Field(..., max_length=200, description="Person responding")
    response_date: Optional[str] = Field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d'))
    send_notification: bool = Field(default=True, description="Send email notification")
    
    @field_validator('response_date')
    @classmethod
    def validate_date(cls, v):
        if v:
            try:
                datetime.strptime(v, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Date must be in YYYY-MM-DD format")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "Thank you for your valuable feedback. We are pleased to hear about your positive experience with our staff. We have noted your concern about wait times and are implementing improvements.",
                "responded_by": "Patient Relations Manager",
                "send_notification": True
            }
        }


# Approve for Publication Schema
class ApproveFeedback(BaseModel):
    """Schema for approving feedback for publication"""
    is_approved: bool = Field(..., description="Approval status")
    is_public: bool = Field(..., description="Make public")
    approved_by: str = Field(..., description="Approver name")
    moderation_notes: Optional[str] = Field(None, description="Internal moderation notes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "is_approved": True,
                "is_public": True,
                "approved_by": "Content Moderator",
                "moderation_notes": "Positive feedback, appropriate for public display"
            }
        }


# Statistics Schema
class FeedbackStats(BaseModel):
    """Feedback statistics"""
    total_feedbacks: int
    recent_feedbacks: int = Field(..., description="Last 30 days")
    pending_response: int
    responded: int
    
    # Ratings
    average_overall_rating: float = Field(..., description="Average overall rating")
    average_staff_rating: Optional[float] = None
    average_cleanliness_rating: Optional[float] = None
    average_facilities_rating: Optional[float] = None
    average_waiting_time_rating: Optional[float] = None
    average_treatment_rating: Optional[float] = None
    
    # Distribution
    ratings_distribution: Dict[str, int] = Field(..., description="Count by rating (1-5)")
    sentiment_distribution: Dict[str, int] = Field(..., description="positive/neutral/negative")
    
    # By service
    feedbacks_by_service: Dict[str, int]
    feedbacks_by_department: Dict[str, int]
    feedbacks_by_source: Dict[str, int]
    
    # Recommendation
    would_recommend_count: int
    would_not_recommend_count: int
    recommendation_rate: float = Field(..., description="Percentage who would recommend")
    
    # Response metrics
    average_response_time_days: Optional[float] = None
    response_rate: float = Field(..., description="Percentage of feedbacks responded to")
    
    # Trends
    trend_last_month: Optional[str] = Field(None, description="improving, declining, stable")
    
    # Top performers
    top_rated_doctors: Optional[List[Dict[str, Any]]] = None
    top_rated_departments: Optional[List[Dict[str, Any]]] = None
    
    # Areas of concern
    lowest_rated_aspects: Optional[List[Dict[str, Any]]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_feedbacks": 1500,
                "recent_feedbacks": 120,
                "pending_response": 15,
                "responded": 1450,
                "average_overall_rating": 4.2,
                "average_staff_rating": 4.5,
                "average_cleanliness_rating": 4.3,
                "average_facilities_rating": 4.0,
                "average_waiting_time_rating": 3.5,
                "average_treatment_rating": 4.6,
                "ratings_distribution": {
                    "5": 600,
                    "4": 500,
                    "3": 250,
                    "2": 100,
                    "1": 50
                },
                "sentiment_distribution": {
                    "positive": 1100,
                    "neutral": 250,
                    "negative": 150
                },
                "feedbacks_by_service": {
                    "consultation": 600,
                    "admission": 400,
                    "emergency": 300,
                    "lab": 200
                },
                "feedbacks_by_department": {
                    "Cardiology": 300,
                    "Orthopedics": 250,
                    "Emergency": 200
                },
                "feedbacks_by_source": {
                    "website": 800,
                    "app": 400,
                    "email": 200,
                    "survey": 100
                },
                "would_recommend_count": 1200,
                "would_not_recommend_count": 150,
                "recommendation_rate": 88.9,
                "average_response_time_days": 2.5,
                "response_rate": 96.7,
                "trend_last_month": "improving",
                "top_rated_doctors": [
                    {"doctor_id": 1, "name": "Dr. Smith", "avg_rating": 4.8, "count": 50}
                ],
                "top_rated_departments": [
                    {"department_id": 1, "name": "Cardiology", "avg_rating": 4.5, "count": 300}
                ],
                "lowest_rated_aspects": [
                    {"aspect": "waiting_time", "avg_rating": 3.5}
                ]
            }
        }


# Dashboard Summary
class FeedbackDashboard(BaseModel):
    """Dashboard summary for feedback"""
    today_feedbacks: int
    this_week_feedbacks: int
    pending_response_count: int
    unread_count: int
    
    # Recent ratings
    today_average_rating: Optional[float] = None
    week_average_rating: Optional[float] = None
    
    # Quick stats
    positive_today: int = Field(..., description="Rating >= 4")
    negative_today: int = Field(..., description="Rating <= 2")
    
    # Recent items
    recent_feedbacks: List[FeedbackResponseSchema] = Field(default=[], max_length=5)
    urgent_feedbacks: List[FeedbackResponseSchema] = Field(default=[], max_length=5, description="Negative ratings needing attention")
    
    # Alerts
    alerts: List[str] = Field(default=[], description="Important alerts")
    
    class Config:
        json_schema_extra = {
            "example": {
                "today_feedbacks": 8,
                "this_week_feedbacks": 45,
                "pending_response_count": 5,
                "unread_count": 3,
                "today_average_rating": 4.3,
                "week_average_rating": 4.1,
                "positive_today": 6,
                "negative_today": 1,
                "recent_feedbacks": [],
                "urgent_feedbacks": [],
                "alerts": [
                    "5 feedbacks awaiting response for >3 days",
                    "2 negative feedbacks require immediate attention"
                ]
            }
        }


# Categorized Feedbacks (for display)
class CategorizedFeedbacks(BaseModel):
    """Feedbacks grouped by service type"""
    service_type: ServiceType
    service_name: str
    feedback_count: int
    average_rating: float
    feedbacks: List[FeedbackResponseSchema]
    
    class Config:
        json_schema_extra = {
            "example": {
                "service_type": "consultation",
                "service_name": "Consultation Services",
                "feedback_count": 150,
                "average_rating": 4.3,
                "feedbacks": []
            }
        }


# Public Testimonials
class PublicTestimonial(BaseModel):
    """Public testimonial (sanitized feedback)"""
    id: int
    patient_name: str = Field(..., description="Name or 'Anonymous'")
    service_type: str
    overall_rating: int
    positive_comments: Optional[str] = None
    would_recommend: bool
    feedback_date: str
    verified: bool = Field(default=True, description="Verified patient")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "patient_name": "John D.",
                "service_type": "consultation",
                "overall_rating": 5,
                "positive_comments": "Excellent care and very professional staff!",
                "would_recommend": True,
                "feedback_date": "2024-01-15",
                "verified": True
            }
        }


class PublicTestimonialList(BaseModel):
    """List of public testimonials"""
    total: int
    average_rating: float
    testimonials: List[PublicTestimonial]


# Report Schema
class FeedbackReport(BaseModel):
    """Feedback report"""
    report_id: str
    report_type: str = Field(..., description="monthly, quarterly, annual, custom")
    period_start: str
    period_end: str
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    generated_by: Optional[str] = None
    
    # Summary
    summary: FeedbackStats
    
    # Detailed analysis
    trends: List[Dict[str, Any]] = Field(default=[], description="Trend analysis")
    insights: List[str] = Field(default=[], description="Key insights")
    recommendations: List[str] = Field(default=[], description="Recommendations")
    action_items: List[Dict[str, Any]] = Field(default=[], description="Action items")
    
    class Config:
        json_schema_extra = {
            "example": {
                "report_id": "RPT-2024-01",
                "report_type": "monthly",
                "period_start": "2024-01-01",
                "period_end": "2024-01-31",
                "generated_at": "2024-02-01T09:00:00",
                "generated_by": "Quality Manager",
                "insights": [
                    "Overall satisfaction improved by 5% compared to last month",
                    "Waiting time ratings remain the lowest scoring category"
                ],
                "recommendations": [
                    "Implement appointment reminder system",
                    "Increase staffing during peak hours"
                ],
                "action_items": [
                    {
                        "item": "Review appointment scheduling system",
                        "assigned_to": "Operations Manager",
                        "priority": "high",
                        "due_date": "2024-02-15"
                    }
                ]
            }
        }


# Export Schema
class FeedbackExport(BaseModel):
    """Export feedbacks"""
    filters: FeedbackFilter = Field(..., description="Filters to apply")
    export_format: str = Field(..., pattern="^(csv|xlsx|pdf|json)$")
    include_patient_info: bool = Field(default=False, description="Include patient details")
    include_responses: bool = Field(default=True)
    anonymize: bool = Field(default=False, description="Remove identifying information")
    filename: Optional[str] = None


# Bulk Operations
class FeedbackBulkStatusUpdate(BaseModel):
    """Bulk update feedback status"""
    feedback_ids: List[int] = Field(..., min_length=1, max_length=50)
    status: FeedbackStatus
    notes: Optional[str] = None
    
    @field_validator('feedback_ids')
    @classmethod
    def validate_ids(cls, v):
        if len(v) > 50:
            raise ValueError("Cannot update more than 50 feedbacks at once")
        return v


class FeedbackBulkApprove(BaseModel):
    """Bulk approve feedbacks"""
    feedback_ids: List[int] = Field(..., min_length=1, max_length=50)
    is_approved: bool
    is_public: bool
    approved_by: str


# NPS (Net Promoter Score) Schema
class NPSScore(BaseModel):
    """Net Promoter Score calculation"""
    total_responses: int
    promoters: int = Field(..., description="Rating 9-10 (would recommend)")
    passives: int = Field(..., description="Rating 7-8")
    detractors: int = Field(..., description="Rating 0-6 (would not recommend)")
    nps_score: float = Field(..., description="NPS = (Promoters - Detractors) / Total * 100")
    category: str = Field(..., description="excellent, good, needs_improvement, poor")
    
    @model_validator(mode='after')
    def calculate_nps(self):
        """Calculate NPS score"""
        if self.total_responses > 0:
            self.nps_score = round(((self.promoters - self.detractors) / self.total_responses) * 100, 2)
            
            # Categorize
            if self.nps_score >= 70:
                self.category = "excellent"
            elif self.nps_score >= 50:
                self.category = "good"
            elif self.nps_score >= 0:
                self.category = "needs_improvement"
            else:
                self.category = "poor"
        
        return self
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_responses": 1000,
                "promoters": 700,
                "passives": 200,
                "detractors": 100,
                "nps_score": 60.0,
                "category": "good"
            }
        }