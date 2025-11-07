"""
Activity Log Schemas
Pydantic schemas for validation and serialization
"""

from pydantic import BaseModel, Field, validator, field_validator
from typing import Optional, Any
from datetime import datetime
from enum import Enum
import json


# Enums
class ActivityType(str, Enum):
    """Valid activity types"""
    LOGIN = "login"
    LOGOUT = "logout"
    PAGE_VIEW = "page_view"
    ACTION = "action"
    DOWNLOAD = "download"
    UPLOAD = "upload"
    SEARCH = "search"
    EXPORT = "export"


class DeviceType(str, Enum):
    """Valid device types"""
    DESKTOP = "desktop"
    MOBILE = "mobile"
    TABLET = "tablet"


class UserType(str, Enum):
    """User types - adjust as per your application"""
    ADMIN = "admin"
    EMPLOYEE = "employee"
    CUSTOMER = "customer"
    GUEST = "guest"


# Base Schema
class ActivityLogBase(BaseModel):
    """Base schema with common fields"""
    user_id: int = Field(..., description="User ID")
    user_name: str = Field(..., max_length=200, description="User name")
    user_type: str = Field(..., max_length=50, description="Type of user")
    activity_type: ActivityType = Field(..., description="Type of activity")
    description: str = Field(..., max_length=500, description="Activity description")
    
    # Optional fields
    metadata: Optional[dict[str, Any]] = Field(None, description="Additional JSON metadata")
    session_id: Optional[str] = Field(None, max_length=100, description="Session identifier")
    ip_address: Optional[str] = Field(None, max_length=50, description="IP address")
    device_type: Optional[DeviceType] = Field(None, description="Device type")
    browser: Optional[str] = Field(None, max_length=100, description="Browser info")
    os: Optional[str] = Field(None, max_length=100, description="Operating system")
    country: Optional[str] = Field(None, max_length=100, description="Country")
    city: Optional[str] = Field(None, max_length=100, description="City")
    duration_seconds: Optional[int] = Field(None, ge=0, description="Duration in seconds")

    @field_validator('metadata', mode='before')
    @classmethod
    def validate_metadata(cls, v):
        """Ensure metadata is valid JSON dict"""
        if v is None:
            return None
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                raise ValueError("Metadata must be valid JSON")
        if isinstance(v, dict):
            return v
        raise ValueError("Metadata must be a dict or JSON string")
    
    @field_validator('ip_address')
    @classmethod
    def validate_ip(cls, v):
        """Basic IP validation"""
        if v is None:
            return None
        # Basic validation - you can use ipaddress module for stricter validation
        parts = v.split('.')
        if len(parts) == 4:  # IPv4
            if all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
                return v
        # Allow IPv6 or other formats
        return v


# Create Schema
class ActivityLogCreate(ActivityLogBase):
    """Schema for creating activity log"""
    pass


# Update Schema (partial updates)
class ActivityLogUpdate(BaseModel):
    """Schema for updating activity log (rarely used)"""
    description: Optional[str] = Field(None, max_length=500)
    metadata: Optional[dict[str, Any]] = None
    duration_seconds: Optional[int] = Field(None, ge=0)

    @field_validator('metadata', mode='before')
    @classmethod
    def validate_metadata(cls, v):
        if v is None:
            return None
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                raise ValueError("Metadata must be valid JSON")
        return v


# Response Schema
class ActivityLogResponse(ActivityLogBase):
    """Schema for activity log response"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True  # Pydantic v2 (use orm_mode = True for Pydantic v1)
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 123,
                "user_name": "John Doe",
                "user_type": "employee",
                "activity_type": "login",
                "description": "User logged in successfully",
                "metadata": {"login_method": "password", "2fa_enabled": True},
                "session_id": "sess_abc123xyz",
                "ip_address": "192.168.1.100",
                "device_type": "desktop",
                "browser": "Chrome 120.0.0",
                "os": "Windows 10",
                "country": "United States",
                "city": "New York",
                "duration_seconds": None,
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00"
            }
        }


# List Response Schema
class ActivityLogListResponse(BaseModel):
    """Schema for paginated list of activity logs"""
    total: int = Field(..., description="Total number of records")
    page: int = Field(..., ge=1, description="Current page number")
    page_size: int = Field(..., ge=1, le=100, description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")
    items: list[ActivityLogResponse] = Field(..., description="Activity log items")


# Filter/Query Schema
class ActivityLogFilter(BaseModel):
    """Schema for filtering activity logs"""
    user_id: Optional[int] = None
    user_name: Optional[str] = None
    user_type: Optional[str] = None
    activity_type: Optional[ActivityType] = None
    session_id: Optional[str] = None
    ip_address: Optional[str] = None
    device_type: Optional[DeviceType] = None
    country: Optional[str] = None
    city: Optional[str] = None
    
    # Date range filters
    created_after: Optional[datetime] = Field(None, description="Filter logs after this date")
    created_before: Optional[datetime] = Field(None, description="Filter logs before this date")
    
    # Pagination
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")
    
    # Sorting
    sort_by: Optional[str] = Field("created_at", description="Field to sort by")
    sort_order: Optional[str] = Field("desc", pattern="^(asc|desc)$", description="Sort order")


# Summary/Stats Schema
class ActivityLogStats(BaseModel):
    """Schema for activity log statistics"""
    total_activities: int
    unique_users: int
    unique_sessions: int
    activities_by_type: dict[str, int]
    activities_by_device: dict[str, int]
    top_users: list[dict[str, Any]]
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_activities": 1500,
                "unique_users": 45,
                "unique_sessions": 120,
                "activities_by_type": {
                    "login": 200,
                    "page_view": 800,
                    "download": 150,
                    "action": 350
                },
                "activities_by_device": {
                    "desktop": 1000,
                    "mobile": 400,
                    "tablet": 100
                },
                "top_users": [
                    {"user_name": "John Doe", "activity_count": 150},
                    {"user_name": "Jane Smith", "activity_count": 120}
                ]
            }
        }


# Bulk Create Schema
class ActivityLogBulkCreate(BaseModel):
    """Schema for creating multiple activity logs"""
    logs: list[ActivityLogCreate] = Field(..., min_length=1, max_length=100)