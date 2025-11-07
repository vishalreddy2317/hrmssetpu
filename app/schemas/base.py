"""
Base Pydantic V2 Schemas
Common schemas and utilities
"""

from typing import Generic, TypeVar, List, Optional, Any
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


# ============================================
# Generic Type Variable
# ============================================

T = TypeVar('T')


# ============================================
# Base Response Models
# ============================================

class ResponseModel(BaseModel):
    """Generic response model"""
    
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
    )
    
    success: bool = True
    message: str = "Operation successful"
    data: Optional[Any] = None


class StatusResponse(BaseModel):
    """Simple status response"""
    
    model_config = ConfigDict(from_attributes=True)
    
    success: bool
    message: str
    status_code: int = 200


class ErrorResponse(BaseModel):
    """Error response model"""
    
    model_config = ConfigDict(from_attributes=True)
    
    success: bool = False
    message: str
    error_code: Optional[str] = None
    details: Optional[dict] = None


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response model"""
    
    model_config = ConfigDict(from_attributes=True)
    
    items: List[T]
    total: int
    page: int = 1
    page_size: int = 20
    total_pages: int
    has_next: bool
    has_prev: bool
    
    @classmethod
    def create(
        cls,
        items: List[T],
        total: int,
        page: int = 1,
        page_size: int = 20
    ):
        """Create paginated response"""
        total_pages = (total + page_size - 1) // page_size
        
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_prev=page > 1
        )


# ============================================
# Base CRUD Schemas
# ============================================

class BaseSchema(BaseModel):
    """Base schema with common configurations"""
    
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        populate_by_name=True,
    )


class TimestampSchema(BaseSchema):
    """Schema with timestamp fields"""
    
    created_at: datetime
    updated_at: datetime


class BaseResponseSchema(TimestampSchema):
    """Base response schema with ID and timestamps"""
    
    id: int
    is_active: bool = True
    is_deleted: bool = False


# ============================================
# Query Parameters
# ============================================

class PaginationParams(BaseModel):
    """Pagination query parameters"""
    
    model_config = ConfigDict(from_attributes=True)
    
    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=20, ge=1, le=100, description="Items per page")
    
    @property
    def skip(self) -> int:
        """Calculate skip value for database query"""
        return (self.page - 1) * self.page_size
    
    @property
    def limit(self) -> int:
        """Get limit value"""
        return self.page_size


class SortParams(BaseModel):
    """Sort query parameters"""
    
    model_config = ConfigDict(from_attributes=True)
    
    sort_by: Optional[str] = Field(default="created_at", description="Field to sort by")
    sort_order: Optional[str] = Field(default="desc", pattern="^(asc|desc)$", description="Sort order")


class FilterParams(BaseModel):
    """Common filter parameters"""
    
    model_config = ConfigDict(from_attributes=True)
    
    search: Optional[str] = Field(default=None, description="Search query")
    status: Optional[str] = Field(default=None, description="Filter by status")
    is_active: Optional[bool] = Field(default=None, description="Filter by active status")
    date_from: Optional[str] = Field(default=None, description="Start date (YYYY-MM-DD)")
    date_to: Optional[str] = Field(default=None, description="End date (YYYY-MM-DD)")


# ============================================
# Common Field Schemas
# ============================================

class AddressSchema(BaseModel):
    """Reusable address schema"""
    
    model_config = ConfigDict(from_attributes=True)
    
    address: str = Field(..., min_length=5, max_length=500)
    city: str = Field(..., min_length=2, max_length=100)
    state: str = Field(..., min_length=2, max_length=100)
    country: str = Field(default="USA", max_length=100)
    pincode: str = Field(..., min_length=3, max_length=20)


class ContactSchema(BaseModel):
    """Reusable contact schema"""
    
    model_config = ConfigDict(from_attributes=True)
    
    phone: str = Field(..., min_length=10, max_length=20)
    alternate_phone: Optional[str] = Field(default=None, max_length=20)
    email: Optional[str] = Field(default=None, max_length=100)


class EmergencyContactSchema(BaseModel):
    """Emergency contact schema"""
    
    model_config = ConfigDict(from_attributes=True)
    
    name: str = Field(..., min_length=2, max_length=200)
    phone: str = Field(..., min_length=10, max_length=20)
    relation: Optional[str] = Field(default=None, max_length=50)


# ============================================
# File Upload Schema
# ============================================

class FileUploadResponse(BaseModel):
    """File upload response"""
    
    model_config = ConfigDict(from_attributes=True)
    
    filename: str
    file_url: str
    file_size: int
    content_type: str
    uploaded_at: datetime


# ============================================
# Statistics Schemas
# ============================================

class CountStatistics(BaseModel):
    """Count statistics"""
    
    model_config = ConfigDict(from_attributes=True)
    
    total: int = 0
    active: int = 0
    inactive: int = 0


class PercentageStatistics(BaseModel):
    """Percentage statistics"""
    
    model_config = ConfigDict(from_attributes=True)
    
    value: float
    percentage: float
    total: int


# ============================================
# Exports
# ============================================

__all__ = [
    "ResponseModel",
    "StatusResponse",
    "ErrorResponse",
    "PaginatedResponse",
    "BaseSchema",
    "TimestampSchema",
    "BaseResponseSchema",
    "PaginationParams",
    "SortParams",
    "FilterParams",
    "AddressSchema",
    "ContactSchema",
    "EmergencyContactSchema",
    "FileUploadResponse",
    "CountStatistics",
    "PercentageStatistics",
]
