"""
Message Schemas
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


# Base Schema
class MessageBase(BaseModel):
    subject: str = Field(..., max_length=200)
    body: str = Field(..., description="Message content")


# Create Schema
class MessageCreate(MessageBase):
    sender_id: int = Field(..., gt=0)
    sender_name: str = Field(..., max_length=200)
    sender_type: str = Field(..., max_length=20)
    
    recipient_id: int = Field(..., gt=0)
    recipient_name: str = Field(..., max_length=200)
    recipient_type: str = Field(..., max_length=20)
    
    message_type: str = Field(default='direct', max_length=50)
    parent_message_id: Optional[int] = None
    thread_id: Optional[str] = Field(None, max_length=50)
    
    priority: str = Field(default='normal', max_length=20)
    attachments: Optional[str] = Field(None, description="JSON array")
    
    is_draft: bool = Field(default=False)
    
    @validator('message_type')
    def validate_message_type(cls, v):
        valid = ['direct', 'broadcast', 'announcement', 'reply']
        if v.lower() not in valid:
            raise ValueError(f"Message type must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validator('priority')
    def validate_priority(cls, v):
        valid = ['low', 'normal', 'high', 'urgent']
        if v.lower() not in valid:
            raise ValueError(f"Priority must be one of: {', '.join(valid)}")
        return v.lower()


# Update Schema
class MessageUpdate(BaseModel):
    subject: Optional[str] = Field(None, max_length=200)
    body: Optional[str] = None
    is_read: Optional[bool] = None
    is_starred: Optional[bool] = None
    is_archived: Optional[bool] = None


# Response Schema
class MessageResponse(MessageBase):
    id: int
    sender_id: int
    sender_name: str
    sender_type: str
    
    recipient_id: int
    recipient_name: str
    recipient_type: str
    
    message_type: str
    parent_message_id: Optional[int]
    thread_id: Optional[str]
    
    is_read: bool
    read_at: Optional[str]
    
    is_starred: bool
    is_archived: bool
    is_draft: bool
    
    priority: str
    attachments: Optional[str]
    
    deleted_by_sender: bool
    deleted_by_recipient: bool
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# List Response
class MessageListResponse(BaseModel):
    total: int
    unread_count: int
    items: list[MessageResponse]
    page: int
    page_size: int
    total_pages: int


# Mark as Read Schema
class MessageMarkReadSchema(BaseModel):
    read_at: Optional[str] = Field(None, max_length=50)


# Reply Schema
class MessageReplySchema(BaseModel):
    body: str = Field(..., description="Reply message content")
    attachments: Optional[str] = Field(None, description="JSON array")