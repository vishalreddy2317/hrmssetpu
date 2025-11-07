"""
Audit Log Schemas
Pydantic schemas for system audit trail and activity logging
"""

from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from typing import Optional, Any, List, Dict, Union
from datetime import datetime, timedelta
from enum import Enum
import json
import re


# Enums
class AuditAction(str, Enum):
    """Valid audit actions"""
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"
    VIEW = "view"
    EXPORT = "export"
    APPROVE = "approve"
    REJECT = "reject"
    SEND = "send"
    DOWNLOAD = "download"
    UPLOAD = "upload"
    RESTORE = "restore"
    ARCHIVE = "archive"
    IMPORT = "import"
    PRINT = "print"


class AuditStatus(str, Enum):
    """Audit log status"""
    SUCCESS = "success"
    FAILURE = "failure"
    ERROR = "error"


class ResourceType(str, Enum):
    """Common resource types"""
    USER = "user"
    PATIENT = "patient"
    DOCTOR = "doctor"
    NURSE = "nurse"
    STAFF = "staff"
    APPOINTMENT = "appointment"
    ADMISSION = "admission"
    DISCHARGE = "discharge"
    MEDICAL_RECORD = "medical_record"
    PRESCRIPTION = "prescription"
    LAB_TEST = "lab_test"
    BILLING = "billing"
    INVOICE = "invoice"
    PAYMENT = "payment"
    ATTENDANCE = "attendance"
    LEAVE = "leave"
    SHIFT = "shift"
    DEPARTMENT = "department"
    ROOM = "room"
    BED = "bed"
    AMBULANCE = "ambulance"
    INVENTORY = "inventory"
    MEDICINE = "medicine"
    EQUIPMENT = "equipment"
    API_KEY = "api_key"
    SETTINGS = "settings"
    REPORT = "report"
    NOTIFICATION = "notification"
    EMAIL = "email"
    SMS = "sms"


class SeverityLevel(str, Enum):
    """Severity levels for audit events"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# Helper Schemas
class FieldChange(BaseModel):
    """Individual field change tracking"""
    field_name: str = Field(..., description="Field that was changed")
    old_value: Any = Field(None, description="Previous value")
    new_value: Any = Field(None, description="New value")
    data_type: Optional[str] = Field(None, description="Data type of the field")
    
    class Config:
        json_schema_extra = {
            "example": {
                "field_name": "status",
                "old_value": "pending",
                "new_value": "confirmed",
                "data_type": "string"
            }
        }


class ChangeSet(BaseModel):
    """Complete change set with metadata"""
    changes: List[FieldChange] = Field(default=[], description="List of field changes")
    total_changes: int = Field(default=0, description="Total number of changes")
    change_summary: Optional[str] = Field(None, description="Human-readable summary")
    
    @model_validator(mode='after')
    def set_total_changes(self):
        self.total_changes = len(self.changes)
        return self
    
    class Config:
        json_schema_extra = {
            "example": {
                "changes": [
                    {
                        "field_name": "status",
                        "old_value": "pending",
                        "new_value": "confirmed"
                    },
                    {
                        "field_name": "amount",
                        "old_value": 100.00,
                        "new_value": 150.00
                    }
                ],
                "total_changes": 2,
                "change_summary": "Updated status and amount"
            }
        }


class RequestContext(BaseModel):
    """HTTP request context information"""
    method: str = Field(..., pattern="^(GET|POST|PUT|PATCH|DELETE|OPTIONS|HEAD)$", description="HTTP method")
    path: str = Field(..., max_length=500, description="Request path")
    ip_address: Optional[str] = Field(None, max_length=50, description="Client IP address")
    user_agent: Optional[str] = Field(None, max_length=500, description="User agent string")
    query_params: Optional[Dict[str, Any]] = Field(None, description="Query parameters")
    headers: Optional[Dict[str, str]] = Field(None, description="Request headers")
    body_size: Optional[int] = Field(None, description="Request body size in bytes")
    response_status: Optional[int] = Field(None, description="HTTP response status code")
    response_time_ms: Optional[int] = Field(None, description="Response time in milliseconds")
    
    @field_validator('ip_address')
    @classmethod
    def validate_ip(cls, v):
        """Validate IP address format"""
        if v is None:
            return None
        # Basic validation for IPv4 and IPv6
        ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        ipv6_pattern = r'^([0-9a-fA-F:]+)$'
        if not (re.match(ipv4_pattern, v) or re.match(ipv6_pattern, v)):
            raise ValueError("Invalid IP address format")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "method": "POST",
                "path": "/api/v1/patients",
                "ip_address": "192.168.1.100",
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "query_params": {"page": 1, "limit": 20},
                "headers": {"Content-Type": "application/json"},
                "body_size": 1024,
                "response_status": 201,
                "response_time_ms": 150
            }
        }


class UserContext(BaseModel):
    """User context information"""
    user_id: Optional[int] = None
    username: Optional[str] = Field(None, max_length=200)
    user_type: Optional[str] = Field(None, max_length=50)
    email: Optional[str] = None
    full_name: Optional[str] = None
    roles: Optional[List[str]] = Field(None, description="User roles")
    permissions: Optional[List[str]] = Field(None, description="User permissions")
    session_id: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 123,
                "username": "john.doe",
                "user_type": "admin",
                "email": "john.doe@example.com",
                "full_name": "John Doe",
                "roles": ["admin", "doctor"],
                "permissions": ["read:all", "write:all"],
                "session_id": "sess_abc123xyz"
            }
        }


class ResourceInfo(BaseModel):
    """Resource information"""
    resource_type: str = Field(..., max_length=100, description="Type of resource")
    resource_id: Optional[int] = Field(None, description="Resource ID")
    resource_name: Optional[str] = Field(None, max_length=200, description="Resource name/identifier")
    resource_url: Optional[str] = Field(None, description="Resource URL")
    parent_resource_type: Optional[str] = Field(None, description="Parent resource type")
    parent_resource_id: Optional[int] = Field(None, description="Parent resource ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "resource_type": "patient",
                "resource_id": 456,
                "resource_name": "Jane Smith",
                "resource_url": "/api/v1/patients/456",
                "parent_resource_type": "hospital",
                "parent_resource_id": 1
            }
        }


# Base Schema
class AuditLogBase(BaseModel):
    """Base schema for audit log"""
    # User/Actor
    user_id: Optional[int] = Field(None, description="User ID who performed the action")
    username: Optional[str] = Field(None, max_length=200, description="Username")
    user_type: Optional[str] = Field(None, max_length=50, description="User type (admin, doctor, etc.)")
    
    # Action
    action: AuditAction = Field(..., description="Action performed")
    
    # Resource
    resource_type: str = Field(..., max_length=100, description="Type of resource affected")
    resource_id: Optional[int] = Field(None, description="ID of the resource")
    resource_name: Optional[str] = Field(None, max_length=200, description="Name/identifier of resource")
    
    # Details
    description: str = Field(..., min_length=1, description="Human-readable description of the action")
    
    # Changes (before/after)
    old_values: Optional[Dict[str, Any]] = Field(None, description="Previous values (JSON)")
    new_values: Optional[Dict[str, Any]] = Field(None, description="New values (JSON)")
    
    # Request Details
    ip_address: Optional[str] = Field(None, max_length=50, description="Client IP address")
    user_agent: Optional[str] = Field(None, max_length=500, description="User agent string")
    request_method: Optional[str] = Field(None, max_length=10, description="HTTP method")
    request_path: Optional[str] = Field(None, max_length=500, description="Request path/URL")
    
    # Status
    status: AuditStatus = Field(default=AuditStatus.SUCCESS, description="Status of the action")
    
    # Error Details
    error_message: Optional[str] = Field(None, description="Error message if action failed")

    @field_validator('old_values', 'new_values', mode='before')
    @classmethod
    def validate_json_values(cls, v):
        """Validate and parse JSON values"""
        if v is None:
            return None
        
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                raise ValueError("Values must be valid JSON")
        
        if isinstance(v, dict):
            return v
        
        raise ValueError("Values must be a dictionary or valid JSON string")
    
    @field_validator('ip_address')
    @classmethod
    def validate_ip_address(cls, v):
        """Validate IP address"""
        if v is None:
            return None
        
        # IPv4 or IPv6 validation
        ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        ipv6_pattern = r'^([0-9a-fA-F:]+)$'
        
        if not (re.match(ipv4_pattern, v) or re.match(ipv6_pattern, v)):
            raise ValueError("Invalid IP address format")
        
        return v
    
    @field_validator('request_method')
    @classmethod
    def validate_http_method(cls, v):
        """Validate HTTP method"""
        if v is None:
            return None
        
        valid_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD']
        if v.upper() not in valid_methods:
            raise ValueError(f"Invalid HTTP method. Must be one of: {', '.join(valid_methods)}")
        
        return v.upper()


# Create Schema
class AuditLogCreate(AuditLogBase):
    """Schema for creating audit log entry"""
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 123,
                "username": "john.doe",
                "user_type": "admin",
                "action": "update",
                "resource_type": "patient",
                "resource_id": 456,
                "resource_name": "Jane Smith",
                "description": "Updated patient contact information",
                "old_values": {
                    "phone": "555-1234",
                    "email": "old@example.com"
                },
                "new_values": {
                    "phone": "555-5678",
                    "email": "new@example.com"
                },
                "ip_address": "192.168.1.100",
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "request_method": "PATCH",
                "request_path": "/api/v1/patients/456",
                "status": "success"
            }
        }


# Detailed Create Schema with Context
class AuditLogCreateDetailed(BaseModel):
    """Detailed schema for creating audit log with full context"""
    # User Context
    user_context: UserContext = Field(..., description="User context information")
    
    # Action
    action: AuditAction = Field(..., description="Action performed")
    
    # Resource
    resource: ResourceInfo = Field(..., description="Resource information")
    
    # Description
    description: str = Field(..., description="Action description")
    
    # Changes
    changes: Optional[ChangeSet] = Field(None, description="Detailed change set")
    
    # Request Context
    request_context: Optional[RequestContext] = Field(None, description="Request context")
    
    # Status
    status: AuditStatus = Field(default=AuditStatus.SUCCESS)
    error_message: Optional[str] = None
    
    # Additional Metadata
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    tags: Optional[List[str]] = Field(None, description="Tags for categorization")
    severity: Optional[SeverityLevel] = Field(None, description="Event severity")


# Response Schema
class AuditLogResponse(AuditLogBase):
    """Schema for audit log response"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 123,
                "username": "john.doe",
                "user_type": "admin",
                "action": "update",
                "resource_type": "patient",
                "resource_id": 456,
                "resource_name": "Jane Smith",
                "description": "Updated patient contact information",
                "old_values": {"phone": "555-1234"},
                "new_values": {"phone": "555-5678"},
                "ip_address": "192.168.1.100",
                "user_agent": "Mozilla/5.0",
                "request_method": "PATCH",
                "request_path": "/api/v1/patients/456",
                "status": "success",
                "error_message": None,
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00"
            }
        }


# Enhanced Response with Calculated Fields
class AuditLogEnhancedResponse(AuditLogResponse):
    """Enhanced response with calculated fields"""
    changes_count: Optional[int] = Field(None, description="Number of fields changed")
    change_summary: Optional[str] = Field(None, description="Summary of changes")
    time_since: Optional[str] = Field(None, description="Human-readable time since event")
    severity: Optional[SeverityLevel] = Field(None, description="Calculated severity")
    
    @model_validator(mode='after')
    def calculate_fields(self):
        """Calculate additional fields"""
        # Calculate changes count
        if self.old_values and self.new_values:
            self.changes_count = len(set(self.old_values.keys()) | set(self.new_values.keys()))
        
        # Calculate time since
        if self.created_at:
            delta = datetime.utcnow() - self.created_at
            if delta.days > 0:
                self.time_since = f"{delta.days} days ago"
            elif delta.seconds > 3600:
                self.time_since = f"{delta.seconds // 3600} hours ago"
            elif delta.seconds > 60:
                self.time_since = f"{delta.seconds // 60} minutes ago"
            else:
                self.time_since = "Just now"
        
        # Determine severity
        if self.action in [AuditAction.DELETE, AuditAction.LOGOUT] or self.status == AuditStatus.ERROR:
            self.severity = SeverityLevel.HIGH
        elif self.action in [AuditAction.UPDATE, AuditAction.APPROVE]:
            self.severity = SeverityLevel.MEDIUM
        else:
            self.severity = SeverityLevel.LOW
        
        return self


# List Response Schema
class AuditLogListResponse(BaseModel):
    """Schema for paginated list of audit logs"""
    total: int = Field(..., description="Total number of records")
    page: int = Field(..., ge=1, description="Current page number")
    page_size: int = Field(..., ge=1, le=500, description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")
    items: List[AuditLogResponse] = Field(..., description="Audit log items")
    filters_applied: Optional[Dict[str, Any]] = Field(None, description="Applied filters")


# Filter/Query Schema
class AuditLogFilter(BaseModel):
    """Schema for filtering audit logs"""
    # User filters
    user_id: Optional[int] = Field(None, description="Filter by user ID")
    username: Optional[str] = Field(None, description="Filter by username (partial match)")
    user_type: Optional[str] = Field(None, description="Filter by user type")
    
    # Action filters
    action: Optional[Union[AuditAction, List[AuditAction]]] = Field(None, description="Filter by action(s)")
    status: Optional[Union[AuditStatus, List[AuditStatus]]] = Field(None, description="Filter by status(es)")
    
    # Resource filters
    resource_type: Optional[Union[str, List[str]]] = Field(None, description="Filter by resource type(s)")
    resource_id: Optional[int] = Field(None, description="Filter by resource ID")
    resource_name: Optional[str] = Field(None, description="Filter by resource name (partial match)")
    
    # Request filters
    ip_address: Optional[str] = Field(None, description="Filter by IP address")
    request_method: Optional[str] = Field(None, description="Filter by HTTP method")
    request_path: Optional[str] = Field(None, description="Filter by request path (partial match)")
    
    # Date/Time filters
    date_from: Optional[datetime] = Field(None, description="From datetime")
    date_to: Optional[datetime] = Field(None, description="To datetime")
    created_after: Optional[datetime] = Field(None, description="Created after")
    created_before: Optional[datetime] = Field(None, description="Created before")
    last_n_hours: Optional[int] = Field(None, gt=0, description="Last N hours")
    last_n_days: Optional[int] = Field(None, gt=0, description="Last N days")
    
    # Error filters
    has_errors: Optional[bool] = Field(None, description="Filter logs with errors")
    
    # Search
    search: Optional[str] = Field(None, min_length=1, description="Search in description, resource_name, username")
    
    # Advanced filters
    changed_field: Optional[str] = Field(None, description="Filter by specific changed field")
    has_changes: Optional[bool] = Field(None, description="Filter logs with/without changes")
    
    # Pagination
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(50, ge=1, le=500, description="Items per page")
    
    # Sorting
    sort_by: Optional[str] = Field("created_at", description="Field to sort by")
    sort_order: Optional[str] = Field("desc", pattern="^(asc|desc)$", description="Sort order (asc/desc)")
    
    # Export
    export_format: Optional[str] = Field(None, pattern="^(json|csv|xlsx|pdf)$", description="Export format")

    @model_validator(mode='after')
    def validate_date_range(self):
        """Validate date range"""
        if self.date_from and self.date_to:
            if self.date_from > self.date_to:
                raise ValueError("date_from must be before date_to")
        
        if self.created_after and self.created_before:
            if self.created_after > self.created_before:
                raise ValueError("created_after must be before created_before")
        
        return self
    
    @model_validator(mode='after')
    def set_date_from_relative(self):
        """Set date_from based on relative filters"""
        if self.last_n_hours:
            self.date_from = datetime.utcnow() - timedelta(hours=self.last_n_hours)
        elif self.last_n_days:
            self.date_from = datetime.utcnow() - timedelta(days=self.last_n_days)
        
        return self


# Statistics Schema
class AuditLogStats(BaseModel):
    """Schema for audit log statistics"""
    total_logs: int = Field(..., description="Total audit logs")
    logs_today: int = Field(..., description="Logs created today")
    logs_this_week: int = Field(..., description="Logs created this week")
    logs_this_month: int = Field(..., description="Logs created this month")
    
    # Breakdowns
    actions_breakdown: Dict[str, int] = Field(..., description="Count by action type")
    status_breakdown: Dict[str, int] = Field(..., description="Count by status")
    resource_type_breakdown: Dict[str, int] = Field(..., description="Count by resource type")
    user_type_breakdown: Dict[str, int] = Field(..., description="Count by user type")
    
    # Top entities
    top_users: List[Dict[str, Any]] = Field(..., description="Most active users")
    top_resources: List[Dict[str, Any]] = Field(..., description="Most accessed resources")
    top_ip_addresses: List[Dict[str, Any]] = Field(..., description="Most active IP addresses")
    
    # Error statistics
    failed_actions: int = Field(..., description="Number of failed actions")
    error_rate: float = Field(..., description="Error rate percentage")
    success_rate: float = Field(..., description="Success rate percentage")
    
    # Trends
    hourly_trend: Optional[List[Dict[str, Any]]] = Field(None, description="Hourly activity trend")
    daily_trend: Optional[List[Dict[str, Any]]] = Field(None, description="Daily activity trend")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_logs": 150000,
                "logs_today": 1500,
                "logs_this_week": 10000,
                "logs_this_month": 45000,
                "actions_breakdown": {
                    "view": 80000,
                    "update": 40000,
                    "create": 20000,
                    "delete": 10000
                },
                "status_breakdown": {
                    "success": 145000,
                    "failure": 3000,
                    "error": 2000
                },
                "resource_type_breakdown": {
                    "patient": 60000,
                    "appointment": 50000,
                    "user": 30000,
                    "billing": 10000
                },
                "user_type_breakdown": {
                    "doctor": 70000,
                    "admin": 50000,
                    "nurse": 30000
                },
                "top_users": [
                    {"user_id": 1, "username": "admin", "action_count": 5000},
                    {"user_id": 2, "username": "doctor1", "action_count": 3000}
                ],
                "top_resources": [
                    {"resource_type": "patient", "count": 60000},
                    {"resource_type": "appointment", "count": 50000}
                ],
                "top_ip_addresses": [
                    {"ip_address": "192.168.1.100", "count": 2000},
                    {"ip_address": "10.0.0.1", "count": 1500}
                ],
                "failed_actions": 5000,
                "error_rate": 3.33,
                "success_rate": 96.67,
                "hourly_trend": [
                    {"hour": 9, "count": 500},
                    {"hour": 10, "count": 800}
                ],
                "daily_trend": [
                    {"date": "2024-01-15", "count": 1500},
                    {"date": "2024-01-14", "count": 1400}
                ]
            }
        }


# User Activity Summary
class UserActivitySummary(BaseModel):
    """User activity summary from audit logs"""
    user_id: int
    username: str
    user_type: Optional[str] = None
    
    # Activity counts
    total_actions: int = Field(..., description="Total actions performed")
    actions_today: int = Field(..., description="Actions today")
    actions_this_week: int = Field(..., description="Actions this week")
    actions_this_month: int = Field(..., description="Actions this month")
    
    # Action breakdown
    actions_by_type: Dict[str, int] = Field(..., description="Count by action type")
    resources_accessed: Dict[str, int] = Field(..., description="Count by resource type")
    
    # Timestamps
    first_activity: Optional[datetime] = Field(None, description="First recorded activity")
    last_activity: Optional[datetime] = Field(None, description="Most recent activity")
    
    # Patterns
    most_common_action: Optional[str] = Field(None, description="Most frequently performed action")
    most_accessed_resource: Optional[str] = Field(None, description="Most accessed resource type")
    peak_activity_hour: Optional[int] = Field(None, description="Hour with most activity (0-23)")
    
    # IP addresses
    unique_ip_addresses: int = Field(default=0, description="Number of unique IP addresses")
    ip_addresses: Optional[List[str]] = Field(None, description="List of IP addresses used")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 123,
                "username": "john.doe",
                "user_type": "admin",
                "total_actions": 5000,
                "actions_today": 50,
                "actions_this_week": 300,
                "actions_this_month": 1200,
                "actions_by_type": {
                    "view": 3000,
                    "update": 1500,
                    "create": 500
                },
                "resources_accessed": {
                    "patient": 2000,
                    "appointment": 1800,
                    "medical_record": 1200
                },
                "first_activity": "2023-01-01T08:00:00",
                "last_activity": "2024-01-15T10:30:00",
                "most_common_action": "view",
                "most_accessed_resource": "patient",
                "peak_activity_hour": 14,
                "unique_ip_addresses": 3,
                "ip_addresses": ["192.168.1.100", "192.168.1.101", "10.0.0.1"]
            }
        }


# Resource Activity Summary
class ResourceActivitySummary(BaseModel):
    """Activity summary for a specific resource"""
    resource_type: str
    resource_id: int
    resource_name: Optional[str] = None
    
    # Activity counts
    total_actions: int = Field(..., description="Total actions on this resource")
    unique_users: int = Field(..., description="Number of unique users who accessed")
    
    # Action breakdown
    actions_by_type: Dict[str, int] = Field(..., description="Count by action type")
    
    # Timestamps
    first_access: Optional[datetime] = Field(None, description="First access time")
    last_access: Optional[datetime] = Field(None, description="Last access time")
    created_at: Optional[datetime] = Field(None, description="Resource creation time")
    last_modified: Optional[datetime] = Field(None, description="Last modification time")
    
    # Change history
    total_modifications: int = Field(default=0, description="Number of modifications")
    fields_changed: Optional[List[str]] = Field(None, description="List of fields that have been changed")
    
    # Access patterns
    top_users: List[Dict[str, Any]] = Field(default=[], description="Users who accessed most")
    
    class Config:
        json_schema_extra = {
            "example": {
                "resource_type": "patient",
                "resource_id": 456,
                "resource_name": "Jane Smith",
                "total_actions": 150,
                "unique_users": 12,
                "actions_by_type": {
                    "view": 100,
                    "update": 40,
                    "export": 10
                },
                "first_access": "2023-06-01T10:00:00",
                "last_access": "2024-01-15T15:30:00",
                "created_at": "2023-06-01T10:00:00",
                "last_modified": "2024-01-14T09:00:00",
                "total_modifications": 40,
                "fields_changed": ["phone", "address", "email", "status"],
                "top_users": [
                    {"user_id": 1, "username": "doctor1", "access_count": 50},
                    {"user_id": 2, "username": "nurse1", "access_count": 30}
                ]
            }
        }


# Security Event Schema
class SecurityEvent(BaseModel):
    """Security-related audit event"""
    event_type: str = Field(..., description="Type of security event")
    severity: SeverityLevel = Field(..., description="Event severity level")
    user_id: Optional[int] = None
    username: Optional[str] = None
    ip_address: Optional[str] = None
    description: str = Field(..., description="Event description")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional event details")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    requires_action: bool = Field(default=False, description="Whether this event requires immediate action")
    action_taken: Optional[str] = Field(None, description="Action taken in response")
    
    class Config:
        json_schema_extra = {
            "example": {
                "event_type": "failed_login_attempts",
                "severity": "high",
                "user_id": 123,
                "username": "john.doe",
                "ip_address": "192.168.1.100",
                "description": "Multiple failed login attempts detected",
                "details": {
                    "attempt_count": 5,
                    "time_window": "5 minutes",
                    "lockout_triggered": True
                },
                "timestamp": "2024-01-15T10:30:00",
                "requires_action": True,
                "action_taken": "Account temporarily locked"
            }
        }


# Compliance Report Schema
class ComplianceReport(BaseModel):
    """Compliance audit report"""
    report_id: str = Field(..., description="Unique report identifier")
    report_period_start: datetime = Field(..., description="Report period start date")
    report_period_end: datetime = Field(..., description="Report period end date")
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    generated_by: Optional[str] = None
    
    # Metrics
    total_access_logs: int = Field(..., description="Total access logs in period")
    data_access_count: int = Field(..., description="Number of data access events")
    data_modifications: int = Field(..., description="Number of data modifications")
    data_deletions: int = Field(..., description="Number of deletions")
    data_exports: int = Field(..., description="Number of data exports")
    
    # Security
    unauthorized_attempts: int = Field(..., description="Unauthorized access attempts")
    policy_violations: int = Field(..., description="Policy violations detected")
    security_incidents: int = Field(..., description="Security incidents")
    
    # Compliance score
    compliance_score: float = Field(..., ge=0, le=100, description="Overall compliance score")
    
    # Findings
    findings: List[Dict[str, Any]] = Field(default=[], description="Compliance findings")
    critical_issues: List[Dict[str, Any]] = Field(default=[], description="Critical issues")
    recommendations: List[str] = Field(default=[], description="Recommendations")
    
    # User access
    privileged_access_count: int = Field(default=0, description="Privileged access events")
    external_access_count: int = Field(default=0, description="External access events")
    
    # Data privacy
    patient_data_access: int = Field(default=0, description="Patient data access count")
    phi_access_count: int = Field(default=0, description="PHI access count")
    
    class Config:
        json_schema_extra = {
            "example": {
                "report_id": "COMP-2024-01",
                "report_period_start": "2024-01-01T00:00:00",
                "report_period_end": "2024-01-31T23:59:59",
                "generated_at": "2024-02-01T09:00:00",
                "generated_by": "compliance.officer",
                "total_access_logs": 50000,
                "data_access_count": 40000,
                "data_modifications": 5000,
                "data_deletions": 500,
                "data_exports": 200,
                "unauthorized_attempts": 25,
                "policy_violations": 10,
                "security_incidents": 2,
                "compliance_score": 98.5,
                "findings": [
                    {
                        "category": "access_control",
                        "issue": "Unauthorized access attempts",
                        "count": 25,
                        "severity": "medium",
                        "status": "reviewed"
                    }
                ],
                "critical_issues": [
                    {
                        "issue": "Potential data breach attempt",
                        "timestamp": "2024-01-15T14:30:00",
                        "user_id": 999,
                        "action_taken": "Account suspended"
                    }
                ],
                "recommendations": [
                    "Implement stronger authentication for privileged accounts",
                    "Review and update access policies quarterly",
                    "Conduct security awareness training"
                ],
                "privileged_access_count": 1500,
                "external_access_count": 200,
                "patient_data_access": 35000,
                "phi_access_count": 30000
            }
        }


# Timeline Event
class TimelineEvent(BaseModel):
    """Timeline event for displaying audit history"""
    timestamp: datetime
    event_id: int
    action: str
    user: str
    resource: str
    description: str
    icon: Optional[str] = Field(None, description="Icon name for UI")
    color: Optional[str] = Field(None, description="Color code for UI")
    details: Optional[Dict[str, Any]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "timestamp": "2024-01-15T10:30:00",
                "event_id": 12345,
                "action": "update",
                "user": "Dr. John Doe",
                "resource": "Patient: Jane Smith",
                "description": "Updated patient contact information",
                "icon": "edit",
                "color": "#3498db",
                "details": {
                    "changes": ["phone", "email"],
                    "ip_address": "192.168.1.100"
                }
            }
        }


# Export Schema
class AuditLogExport(BaseModel):
    """Schema for exporting audit logs"""
    filters: AuditLogFilter = Field(..., description="Filters to apply")
    export_format: str = Field(..., pattern="^(json|csv|xlsx|pdf)$", description="Export format")
    include_fields: Optional[List[str]] = Field(None, description="Fields to include in export")
    exclude_fields: Optional[List[str]] = Field(None, description="Fields to exclude from export")
    filename: Optional[str] = Field(None, description="Custom filename")
    
    class Config:
        json_schema_extra = {
            "example": {
                "filters": {
                    "date_from": "2024-01-01T00:00:00",
                    "date_to": "2024-01-31T23:59:59",
                    "action": "update",
                    "resource_type": "patient"
                },
                "export_format": "csv",
                "include_fields": ["timestamp", "user", "action", "resource", "description"],
                "filename": "audit_logs_january_2024.csv"
            }
        }


# Bulk Operations
class AuditLogBulkQuery(BaseModel):
    """Schema for bulk querying audit logs"""
    user_ids: Optional[List[int]] = Field(None, min_length=1, description="List of user IDs")
    resource_ids: Optional[List[int]] = Field(None, min_length=1, description="List of resource IDs")
    date_range: Optional[Dict[str, datetime]] = Field(None, description="Date range")
    actions: Optional[List[AuditAction]] = Field(None, description="List of actions")
    
    @model_validator(mode='after')
    def validate_at_least_one_filter(self):
        """Ensure at least one filter is provided"""
        if not any([self.user_ids, self.resource_ids, self.date_range, self.actions]):
            raise ValueError("At least one filter must be provided")
        return self