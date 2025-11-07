"""
Notification Schemas
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


# Base Schema
class NotificationBase(BaseModel):
    title: str = Field(..., max_length=200)
    message: str = Field(..., description="Notification message")
    notification_type: str = Field(..., max_length=50)
    category: str = Field(..., max_length=50)
    
    @validator('notification_type')
    def validate_notification_type(cls, v):
        valid = ['info', 'warning', 'error', 'success', 'reminder', 'alert']
        if v.lower() not in valid:
            raise ValueError(f"Notification type must be one of: {', '.join(valid)}")
        return v.lower()


# Create Schema
class NotificationCreate(NotificationBase):
    user_id: Optional[int] = None
    recipient_email: Optional[str] = Field(None, max_length=100)
    recipient_phone: Optional[str] = Field(None, max_length=20)
    recipient_type: Optional[str] = Field(None, max_length=20)
    
    send_email: bool = Field(default=True)
    send_sms: bool = Field(default=False)
    send_push: bool = Field(default=True)
    send_in_app: bool = Field(default=True)
    
    priority: str = Field(default='normal', max_length=20)
    
    action_url: Optional[str] = Field(None, max_length=500)
    action_text: Optional[str] = Field(None, max_length=100)
    
    reference_type: Optional[str] = Field(None, max_length=50)
    reference_id: Optional[int] = None
    
    expires_at: Optional[str] = Field(None, max_length=50)
    
    @validator('priority')
    def validate_priority(cls, v):
        valid = ['low', 'normal', 'high', 'urgent']
        if v.lower() not in valid:
            raise ValueError(f"Priority must be one of: {', '.join(valid)}")
        return v.lower()


# Update Schema
class NotificationUpdate(BaseModel):
    is_read: Optional[bool] = None
    read_at: Optional[str] = Field(None, max_length=50)
    email_sent: Optional[bool] = None
    sms_sent: Optional[bool] = None
    push_sent: Optional[bool] = None


# Response Schema
class NotificationResponse(NotificationBase):
    id: int
    user_id: Optional[int]
    recipient_email: Optional[str]
    recipient_phone: Optional[str]
    recipient_type: Optional[str]
    
    send_email: bool
    send_sms: bool
    send_push: bool
    send_in_app: bool
    
    is_read: bool
    read_at: Optional[str]
    
    email_sent: bool
    sms_sent: bool
    push_sent: bool
    
    priority: str
    
    action_url: Optional[str]
    action_text: Optional[str]
    
    reference_type: Optional[str]
    reference_id: Optional[int]
    
    expires_at: Optional[str]
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# List Response
class NotificationListResponse(BaseModel):
    total: int
    unread_count: int
    items: list[NotificationResponse]
    page: int
    page_size: int
    total_pages: int


# Mark as Read Schema
class NotificationMarkReadSchema(BaseModel):
    read_at: Optional[str] = Field(None, max_length=50)


# Bulk Create Schema
class NotificationBulkCreate(BaseModel):
    title: str = Field(..., max_length=200)
    message: str = Field(...)
    notification_type: str = Field(..., max_length=50)
    category: str = Field(..., max_length=50)
    
    user_ids: list[int] = Field(..., description="List of user IDs to send notification")
    
    send_email: bool = Field(default=True)
    send_sms: bool = Field(default=False)
    send_push: bool = Field(default=True)
    send_in_app: bool = Field(default=True)
    
    priority: str = Field(default='normal', max_length=20)
    
    action_url: Optional[str] = Field(None, max_length=500)
    action_text: Optional[str] = Field(None, max_length=100)