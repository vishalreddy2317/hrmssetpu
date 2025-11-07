"""
FAQ Schemas
Pydantic schemas for frequently asked questions management
"""

from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum
import json


# Enums
class FAQCategory(str, Enum):
    """FAQ categories"""
    GENERAL = "general"
    APPOINTMENTS = "appointments"
    BILLING = "billing"
    SERVICES = "services"
    EMERGENCY = "emergency"
    INSURANCE = "insurance"
    PHARMACY = "pharmacy"
    LAB = "lab"
    TECHNICAL = "technical"


class FAQStatus(str, Enum):
    """FAQ status"""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class Language(str, Enum):
    """Supported languages"""
    EN = "en"
    ES = "es"
    FR = "fr"
    DE = "de"
    ZH = "zh"


# Helper Schemas
class RelatedFAQ(BaseModel):
    """Related FAQ reference"""
    id: int
    question: str
    category: str
    
    class Config:
        from_attributes = True


class FAQFeedback(BaseModel):
    """Feedback on FAQ helpfulness"""
    is_helpful: bool = Field(..., description="Whether FAQ was helpful")
    feedback_text: Optional[str] = Field(None, max_length=500, description="Additional feedback")
    user_type: Optional[str] = Field(None, description="Type of user providing feedback")
    submitted_at: datetime = Field(default_factory=datetime.utcnow)


# Base Schema
class FAQBase(BaseModel):
    """Base schema for FAQ"""
    question: str = Field(..., min_length=10, max_length=500, description="Question text")
    answer: str = Field(..., min_length=10, description="Answer text")
    category: FAQCategory = Field(..., description="FAQ category")
    display_order: int = Field(default=0, description="Display order (0 = highest)")
    tags: Optional[str] = Field(None, max_length=500, description="Comma-separated tags")
    status: FAQStatus = Field(default=FAQStatus.PUBLISHED, description="Publication status")
    view_count: int = Field(default=0, ge=0, description="Number of views")
    helpful_count: int = Field(default=0, ge=0, description="Helpful votes")
    not_helpful_count: int = Field(default=0, ge=0, description="Not helpful votes")
    language: str = Field(default="en", max_length=10, description="Language code")
    related_faqs: Optional[List[int]] = Field(None, description="Related FAQ IDs")
    created_by: Optional[str] = Field(None, max_length=200, description="Created by")
    last_updated_by: Optional[str] = Field(None, max_length=200, description="Last updated by")

    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v):
        """Validate and clean tags"""
        if v is None:
            return None
        # Clean up tags: strip whitespace, lowercase
        tags = [tag.strip().lower() for tag in v.split(',') if tag.strip()]
        return ','.join(tags)
    
    @field_validator('related_faqs', mode='before')
    @classmethod
    def parse_related_faqs(cls, v):
        """Parse related FAQs if JSON string"""
        if v is None:
            return None
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                raise ValueError("Related FAQs must be valid JSON array")
        return v
    
    @field_validator('language')
    @classmethod
    def validate_language(cls, v):
        """Validate language code"""
        valid_languages = ['en', 'es', 'fr', 'de', 'zh', 'ar', 'hi', 'pt']
        if v.lower() not in valid_languages:
            raise ValueError(f"Language must be one of: {', '.join(valid_languages)}")
        return v.lower()


# Create Schema
class FAQCreate(BaseModel):
    """Schema for creating FAQ"""
    question: str = Field(..., min_length=10, max_length=500)
    answer: str = Field(..., min_length=10)
    category: FAQCategory
    display_order: int = Field(default=0)
    tags: Optional[str] = Field(None, max_length=500, description="Comma-separated")
    status: FAQStatus = Field(default=FAQStatus.PUBLISHED)
    language: str = Field(default="en")
    related_faqs: Optional[List[int]] = None
    created_by: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "What are your visiting hours?",
                "answer": "Our general visiting hours are from 10:00 AM to 8:00 PM daily. ICU visiting hours are 2:00 PM to 4:00 PM and 7:00 PM to 8:00 PM. Special arrangements can be made for critically ill patients.",
                "category": "general",
                "display_order": 1,
                "tags": "visiting, hours, policy, ICU",
                "status": "published",
                "language": "en"
            }
        }


# Update Schema
class FAQUpdate(BaseModel):
    """Schema for updating FAQ"""
    question: Optional[str] = Field(None, min_length=10, max_length=500)
    answer: Optional[str] = Field(None, min_length=10)
    category: Optional[FAQCategory] = None
    display_order: Optional[int] = None
    tags: Optional[str] = None
    status: Optional[FAQStatus] = None
    language: Optional[str] = None
    related_faqs: Optional[List[int]] = None
    last_updated_by: Optional[str] = None


# Response Schema
class FAQResponse(FAQBase):
    """Schema for FAQ response"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    # Calculated fields
    helpfulness_score: Optional[float] = Field(None, description="Helpfulness percentage")
    total_feedback: int = Field(default=0, description="Total feedback count")
    is_popular: bool = Field(default=False, description="Is in top viewed")
    last_viewed: Optional[datetime] = Field(None, description="Last view timestamp")
    
    model_config = ConfigDict(from_attributes=True)
    
    @model_validator(mode='after')
    def calculate_scores(self):
        """Calculate helpfulness metrics"""
        total = self.helpful_count + self.not_helpful_count
        self.total_feedback = total
        
        if total > 0:
            self.helpfulness_score = round((self.helpful_count / total) * 100, 2)
        
        # Popular if viewed more than 100 times
        self.is_popular = self.view_count > 100
        
        return self
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "question": "What are your visiting hours?",
                "answer": "Our general visiting hours are...",
                "category": "general",
                "status": "published",
                "view_count": 250,
                "helpful_count": 45,
                "not_helpful_count": 5,
                "helpfulness_score": 90.0,
                "is_popular": True,
                "created_at": "2024-01-01T10:00:00",
                "updated_at": "2024-01-15T10:00:00"
            }
        }


# Detail Response with Related FAQs
class FAQDetailResponse(FAQResponse):
    """Detailed FAQ with related FAQs"""
    related_faqs_detail: Optional[List[RelatedFAQ]] = Field(None, description="Related FAQ details")
    
    model_config = ConfigDict(from_attributes=True)


# List Response Schema
class FAQListResponse(BaseModel):
    """Schema for paginated list of FAQs"""
    total: int = Field(..., description="Total number of records")
    page: int = Field(..., ge=1, description="Current page number")
    page_size: int = Field(..., ge=1, le=100, description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")
    items: List[FAQResponse] = Field(..., description="FAQ items")
    categories: Optional[Dict[str, int]] = Field(None, description="FAQ count by category")


# Filter Schema
class FAQFilter(BaseModel):
    """Schema for filtering FAQs"""
    # Category and status
    category: Optional[Union[FAQCategory, List[FAQCategory]]] = Field(None, description="Filter by category")
    status: Optional[Union[FAQStatus, List[FAQStatus]]] = Field(None, description="Filter by status")
    language: Optional[str] = Field(None, description="Filter by language")
    
    # Tags
    tags: Optional[str] = Field(None, description="Filter by tags (comma-separated)")
    
    # Boolean filters
    popular_only: Optional[bool] = Field(None, description="Only popular FAQs (>100 views)")
    highly_rated: Optional[bool] = Field(None, description="Helpfulness > 70%")
    
    # Search
    search: Optional[str] = Field(None, description="Search in question and answer")
    
    # Pagination
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")
    
    # Sorting
    sort_by: str = Field("display_order", description="Field to sort by")
    sort_order: str = Field("asc", pattern="^(asc|desc)$", description="Sort order")
    
    # Include related
    include_related: bool = Field(False, description="Include related FAQ details")


# Submit Feedback Schema
class SubmitFeedback(BaseModel):
    """Schema for submitting FAQ feedback"""
    faq_id: int = Field(..., description="FAQ ID")
    is_helpful: bool = Field(..., description="Was this helpful?")
    feedback_text: Optional[str] = Field(None, max_length=500, description="Additional comments")
    user_type: Optional[str] = Field(None, description="User type (patient, staff, visitor)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "faq_id": 1,
                "is_helpful": True,
                "feedback_text": "Very clear and helpful information",
                "user_type": "patient"
            }
        }


# Record View Schema
class RecordView(BaseModel):
    """Schema for recording FAQ view"""
    faq_id: int = Field(..., description="FAQ ID")
    user_type: Optional[str] = Field(None, description="User type")
    session_id: Optional[str] = Field(None, description="Session ID for tracking")


# Statistics Schema
class FAQStats(BaseModel):
    """FAQ statistics"""
    total_faqs: int
    published_faqs: int
    draft_faqs: int
    archived_faqs: int
    faqs_by_category: Dict[str, int]
    faqs_by_language: Dict[str, int]
    total_views: int
    total_feedback: int
    average_helpfulness: float = Field(..., description="Average helpfulness percentage")
    most_viewed_faqs: List[Dict[str, Any]]
    most_helpful_faqs: List[Dict[str, Any]]
    least_helpful_faqs: List[Dict[str, Any]]
    popular_tags: List[str] = Field(default=[], description="Most used tags")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_faqs": 150,
                "published_faqs": 120,
                "draft_faqs": 20,
                "archived_faqs": 10,
                "faqs_by_category": {
                    "general": 40,
                    "appointments": 30,
                    "billing": 25,
                    "services": 20
                },
                "faqs_by_language": {
                    "en": 120,
                    "es": 20,
                    "fr": 10
                },
                "total_views": 15000,
                "total_feedback": 5000,
                "average_helpfulness": 82.5,
                "most_viewed_faqs": [
                    {"id": 1, "question": "What are your visiting hours?", "views": 500}
                ],
                "most_helpful_faqs": [
                    {"id": 2, "question": "How do I book an appointment?", "helpfulness": 95.0}
                ],
                "least_helpful_faqs": [],
                "popular_tags": ["appointments", "billing", "insurance", "emergency"]
            }
        }


# Categorized FAQs Response
class CategorizedFAQs(BaseModel):
    """FAQs organized by category"""
    category: FAQCategory
    category_name: str
    description: Optional[str] = None
    faq_count: int
    faqs: List[FAQResponse]
    
    class Config:
        json_schema_extra = {
            "example": {
                "category": "appointments",
                "category_name": "Appointments",
                "description": "Questions about scheduling and managing appointments",
                "faq_count": 15,
                "faqs": []
            }
        }


class AllCategorizedFAQs(BaseModel):
    """All FAQs grouped by category"""
    categories: List[CategorizedFAQs]
    total_faqs: int
    total_categories: int


# Bulk Operations
class FAQBulkStatusUpdate(BaseModel):
    """Bulk update FAQ status"""
    faq_ids: List[int] = Field(..., min_length=1, max_length=50)
    status: FAQStatus
    updated_by: Optional[str] = None
    
    @field_validator('faq_ids')
    @classmethod
    def validate_ids(cls, v):
        if len(v) > 50:
            raise ValueError("Cannot update more than 50 FAQs at once")
        return v


class FAQBulkCategoryUpdate(BaseModel):
    """Bulk update FAQ category"""
    faq_ids: List[int] = Field(..., min_length=1, max_length=50)
    category: FAQCategory
    updated_by: Optional[str] = None


# Export Schema
class FAQExport(BaseModel):
    """Export FAQs"""
    filters: FAQFilter = Field(..., description="Filters to apply")
    export_format: str = Field(..., pattern="^(csv|xlsx|pdf|json)$")
    include_feedback: bool = Field(default=False)
    filename: Optional[str] = None


# Import Schema
class FAQImport(BaseModel):
    """Import FAQs from file"""
    file_url: str = Field(..., description="URL of file to import")
    file_format: str = Field(..., pattern="^(csv|xlsx|json)$")
    category: FAQCategory = Field(..., description="Default category for imported FAQs")
    language: str = Field(default="en")
    auto_publish: bool = Field(default=False, description="Auto-publish or save as draft")
    override_existing: bool = Field(default=False)