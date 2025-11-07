"""
Chat Schemas
Pydantic schemas for real-time chat messaging system
"""

from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict, HttpUrl
from typing import Optional, Any, List, Dict, Union
from datetime import datetime, timedelta
from enum import Enum
import json
import re
from uuid import UUID, uuid4


# Enums
class RoomType(str, Enum):
    """Valid room/channel types"""
    DIRECT = "direct"
    GROUP = "group"
    SUPPORT = "support"
    EMERGENCY = "emergency"
    ANNOUNCEMENT = "announcement"
    DEPARTMENT = "department"
    BROADCAST = "broadcast"


class MessageType(str, Enum):
    """Valid message types"""
    TEXT = "text"
    IMAGE = "image"
    FILE = "file"
    AUDIO = "audio"
    VIDEO = "video"
    LOCATION = "location"
    SYSTEM = "system"
    NOTIFICATION = "notification"


class SenderType(str, Enum):
    """Sender types"""
    USER = "user"
    DOCTOR = "doctor"
    NURSE = "nurse"
    PATIENT = "patient"
    STAFF = "staff"
    ADMIN = "admin"
    BOT = "bot"
    SYSTEM = "system"


class MessageStatus(str, Enum):
    """Message delivery status"""
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"


class TypingStatus(str, Enum):
    """Typing indicator status"""
    TYPING = "typing"
    STOPPED = "stopped"


# Helper Schemas
class Attachment(BaseModel):
    """Attachment information"""
    url: str = Field(..., max_length=500, description="Attachment URL")
    type: str = Field(..., max_length=50, description="Attachment MIME type")
    name: Optional[str] = Field(None, max_length=200, description="Original filename")
    size: Optional[int] = Field(None, ge=0, description="File size in bytes")
    thumbnail_url: Optional[str] = Field(None, description="Thumbnail URL for images/videos")
    duration: Optional[int] = Field(None, description="Duration in seconds for audio/video")
    width: Optional[int] = Field(None, description="Width for images/videos")
    height: Optional[int] = Field(None, description="Height for images/videos")
    
    @field_validator('size')
    @classmethod
    def validate_size(cls, v):
        """Validate file size (max 100MB)"""
        if v and v > 100 * 1024 * 1024:
            raise ValueError("File size cannot exceed 100MB")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://cdn.example.com/files/document.pdf",
                "type": "application/pdf",
                "name": "medical_report.pdf",
                "size": 1024000,
                "thumbnail_url": "https://cdn.example.com/thumbs/document.jpg"
            }
        }


class Location(BaseModel):
    """Location/coordinates information"""
    latitude: float = Field(..., ge=-90, le=90, description="Latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude")
    address: Optional[str] = Field(None, max_length=500, description="Human-readable address")
    place_name: Optional[str] = Field(None, max_length=200, description="Place name")
    
    class Config:
        json_schema_extra = {
            "example": {
                "latitude": 40.7128,
                "longitude": -74.0060,
                "address": "123 Main St, New York, NY 10001",
                "place_name": "Central Hospital"
            }
        }


class Reaction(BaseModel):
    """Message reaction"""
    emoji: str = Field(..., min_length=1, max_length=10, description="Emoji character")
    user_id: int = Field(..., description="User who reacted")
    user_name: Optional[str] = Field(None, description="User name")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "emoji": "👍",
                "user_id": 123,
                "user_name": "John Doe",
                "timestamp": "2024-01-15T10:30:00"
            }
        }


class ReactionSummary(BaseModel):
    """Summary of reactions on a message"""
    reactions: Dict[str, List[int]] = Field(
        default={},
        description="Map of emoji to list of user IDs"
    )
    total_count: int = Field(default=0, description="Total reaction count")
    
    class Config:
        json_schema_extra = {
            "example": {
                "reactions": {
                    "👍": [1, 2, 3],
                    "❤️": [4, 5],
                    "😂": [6]
                },
                "total_count": 6
            }
        }


class ReadReceipt(BaseModel):
    """Read receipt information"""
    user_id: int
    user_name: str
    read_at: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 123,
                "user_name": "John Doe",
                "read_at": "2024-01-15T10:30:00"
            }
        }


class RoomParticipant(BaseModel):
    """Chat room participant"""
    user_id: int = Field(..., description="User ID")
    user_name: str = Field(..., max_length=200, description="User name")
    user_type: Optional[SenderType] = Field(None, description="User type")
    avatar_url: Optional[str] = Field(None, description="User avatar URL")
    role: Optional[str] = Field(None, description="Role in room (admin, moderator, member)")
    joined_at: Optional[datetime] = Field(None, description="When user joined the room")
    is_online: bool = Field(default=False, description="Online status")
    last_seen: Optional[datetime] = Field(None, description="Last seen timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 123,
                "user_name": "Dr. John Doe",
                "user_type": "doctor",
                "avatar_url": "https://cdn.example.com/avatars/123.jpg",
                "role": "admin",
                "joined_at": "2024-01-01T10:00:00",
                "is_online": True,
                "last_seen": "2024-01-15T10:30:00"
            }
        }


class RoomSettings(BaseModel):
    """Chat room settings"""
    is_muted: bool = Field(default=False, description="Mute notifications")
    is_pinned: bool = Field(default=False, description="Pin to top")
    notifications_enabled: bool = Field(default=True, description="Enable notifications")
    sound_enabled: bool = Field(default=True, description="Enable sound")
    auto_delete_messages: Optional[int] = Field(None, description="Auto-delete after N days")
    
    class Config:
        json_schema_extra = {
            "example": {
                "is_muted": False,
                "is_pinned": True,
                "notifications_enabled": True,
                "sound_enabled": True,
                "auto_delete_messages": 30
            }
        }


# Base Schema
class ChatBase(BaseModel):
    """Base schema for chat messages"""
    # Room
    room_id: str = Field(..., min_length=1, max_length=50, description="Room/channel identifier")
    room_name: Optional[str] = Field(None, max_length=200, description="Room display name")
    room_type: RoomType = Field(default=RoomType.DIRECT, description="Type of chat room")
    
    # Sender
    sender_id: int = Field(..., description="Sender user ID")
    sender_name: str = Field(..., max_length=200, description="Sender name")
    sender_type: Optional[SenderType] = Field(None, max_length=20, description="Sender type")
    
    # Message
    message: str = Field(..., min_length=1, description="Message content")
    message_type: MessageType = Field(default=MessageType.TEXT, description="Type of message")
    
    # Attachment
    attachment_url: Optional[str] = Field(None, max_length=500, description="Attachment URL")
    attachment_type: Optional[str] = Field(None, max_length=50, description="Attachment MIME type")
    
    # Status
    is_read: bool = Field(default=False, description="Read status")
    read_by: Optional[List[int]] = Field(None, description="List of user IDs who read the message")
    
    # Reply
    reply_to_message_id: Optional[int] = Field(None, description="ID of message being replied to")
    
    # Reactions
    reactions: Optional[Dict[str, List[int]]] = Field(None, description="Reactions map")
    
    # Edit/Delete
    is_edited: bool = Field(default=False, description="Whether message was edited")
    edited_at: Optional[datetime] = Field(None, description="When message was edited")
    is_deleted: bool = Field(default=False, description="Soft delete flag")

    @field_validator('read_by', 'reactions', mode='before')
    @classmethod
    def parse_json_fields(cls, v):
        """Parse JSON fields if they come as strings"""
        if v is None:
            return None
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON format")
        return v
    
    @field_validator('message')
    @classmethod
    def validate_message_length(cls, v):
        """Validate message length"""
        if len(v) > 10000:
            raise ValueError("Message cannot exceed 10000 characters")
        return v
    
    @model_validator(mode='after')
    def validate_attachment_consistency(self):
        """Ensure attachment fields are consistent"""
        if self.message_type != MessageType.TEXT:
            if not self.attachment_url:
                raise ValueError(f"attachment_url required for {self.message_type} messages")
        return self


# Create Schema
class ChatCreate(BaseModel):
    """Schema for creating new chat message"""
    room_id: str = Field(..., min_length=1, max_length=50)
    room_name: Optional[str] = Field(None, max_length=200)
    room_type: RoomType = Field(default=RoomType.DIRECT)
    sender_id: int
    sender_name: str = Field(..., max_length=200)
    sender_type: Optional[SenderType] = None
    message: str = Field(..., min_length=1, max_length=10000)
    message_type: MessageType = Field(default=MessageType.TEXT)
    attachment: Optional[Attachment] = Field(None, description="Attachment details")
    location: Optional[Location] = Field(None, description="Location details for location messages")
    reply_to_message_id: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "room_id": "room_123_456",
                "room_name": "Dr. Smith & Patient John",
                "room_type": "direct",
                "sender_id": 123,
                "sender_name": "Dr. John Smith",
                "sender_type": "doctor",
                "message": "Hello, how are you feeling today?",
                "message_type": "text",
                "reply_to_message_id": None
            }
        }


# Update Schema
class ChatUpdate(BaseModel):
    """Schema for updating chat message (editing)"""
    message: str = Field(..., min_length=1, max_length=10000, description="Updated message content")
    edited_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Hello, how are you feeling today? (edited)",
                "edited_at": "2024-01-15T10:35:00"
            }
        }


# Response Schema
class ChatResponse(ChatBase):
    """Schema for chat message response"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    # Enhanced fields
    sender_avatar: Optional[str] = Field(None, description="Sender avatar URL")
    delivery_status: Optional[MessageStatus] = Field(None, description="Delivery status")
    
    model_config = ConfigDict(from_attributes=True)
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "room_id": "room_123_456",
                "room_name": "Dr. Smith & Patient John",
                "room_type": "direct",
                "sender_id": 123,
                "sender_name": "Dr. John Smith",
                "sender_type": "doctor",
                "message": "Hello, how are you feeling today?",
                "message_type": "text",
                "is_read": False,
                "is_edited": False,
                "is_deleted": False,
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00"
            }
        }


# Enhanced Response with Relationships
class ChatDetailResponse(ChatResponse):
    """Detailed chat message with relationships"""
    reply_to_message: Optional['ChatResponse'] = Field(None, description="Replied message details")
    read_receipts: List[ReadReceipt] = Field(default=[], description="Read receipts")
    reaction_summary: Optional[ReactionSummary] = Field(None, description="Reaction summary")
    attachment_details: Optional[Attachment] = Field(None, description="Full attachment details")
    location_details: Optional[Location] = Field(None, description="Location details")
    
    model_config = ConfigDict(from_attributes=True)


# List Response Schema
class ChatListResponse(BaseModel):
    """Schema for paginated list of chat messages"""
    total: int = Field(..., description="Total number of messages")
    page: int = Field(..., ge=1, description="Current page number")
    page_size: int = Field(..., ge=1, le=100, description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")
    items: List[ChatResponse] = Field(..., description="Chat messages")
    has_more: bool = Field(..., description="Whether there are more messages")


# Filter Schema
class ChatFilter(BaseModel):
    """Schema for filtering chat messages"""
    # Room filter
    room_id: Optional[str] = Field(None, description="Filter by room ID")
    room_type: Optional[RoomType] = Field(None, description="Filter by room type")
    
    # Sender filter
    sender_id: Optional[int] = Field(None, description="Filter by sender ID")
    sender_type: Optional[SenderType] = Field(None, description="Filter by sender type")
    
    # Message type filter
    message_type: Optional[MessageType] = Field(None, description="Filter by message type")
    
    # Status filters
    is_read: Optional[bool] = Field(None, description="Filter by read status")
    is_edited: Optional[bool] = Field(None, description="Filter edited messages")
    is_deleted: Optional[bool] = Field(None, description="Include deleted messages")
    
    # Date filters
    date_from: Optional[datetime] = Field(None, description="Messages from this date")
    date_to: Optional[datetime] = Field(None, description="Messages until this date")
    before_message_id: Optional[int] = Field(None, description="Messages before this ID (for pagination)")
    after_message_id: Optional[int] = Field(None, description="Messages after this ID")
    
    # Search
    search: Optional[str] = Field(None, min_length=1, description="Search in message content")
    has_attachments: Optional[bool] = Field(None, description="Filter messages with attachments")
    
    # Pagination
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(50, ge=1, le=100, description="Items per page")
    
    # Sorting
    sort_order: str = Field("desc", pattern="^(asc|desc)$", description="Sort order")


# Room Schema
class ChatRoomBase(BaseModel):
    """Base schema for chat room"""
    room_id: str = Field(..., min_length=1, max_length=50, description="Unique room identifier")
    room_name: str = Field(..., min_length=1, max_length=200, description="Room display name")
    room_type: RoomType = Field(..., description="Type of room")
    description: Optional[str] = Field(None, max_length=500, description="Room description")
    avatar_url: Optional[str] = Field(None, description="Room avatar/icon URL")
    created_by: int = Field(..., description="User ID who created the room")
    participants: List[int] = Field(..., min_length=1, description="List of participant user IDs")
    admins: Optional[List[int]] = Field(None, description="List of admin user IDs")
    settings: Optional[RoomSettings] = Field(None, description="Room settings")
    is_active: bool = Field(default=True, description="Whether room is active")
    
    class Config:
        json_schema_extra = {
            "example": {
                "room_id": "room_123_456",
                "room_name": "Dr. Smith & Patient John",
                "room_type": "direct",
                "description": "Direct chat between doctor and patient",
                "created_by": 123,
                "participants": [123, 456],
                "is_active": True
            }
        }


class ChatRoomCreate(ChatRoomBase):
    """Schema for creating chat room"""
    pass


class ChatRoomResponse(ChatRoomBase):
    """Schema for chat room response"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    # Additional fields
    participant_details: Optional[List[RoomParticipant]] = Field(None, description="Full participant details")
    last_message: Optional[ChatResponse] = Field(None, description="Last message in room")
    unread_count: int = Field(default=0, description="Unread message count for current user")
    total_messages: int = Field(default=0, description="Total messages in room")
    
    model_config = ConfigDict(from_attributes=True)


class ChatRoomListResponse(BaseModel):
    """Schema for list of chat rooms"""
    total: int
    items: List[ChatRoomResponse]


# WebSocket Schemas
class WSMessageType(str, Enum):
    """WebSocket message types"""
    MESSAGE = "message"
    TYPING = "typing"
    READ_RECEIPT = "read_receipt"
    REACTION = "reaction"
    DELETE = "delete"
    EDIT = "edit"
    USER_JOINED = "user_joined"
    USER_LEFT = "user_left"
    USER_ONLINE = "user_online"
    USER_OFFLINE = "user_offline"
    ERROR = "error"
    PING = "ping"
    PONG = "pong"


class WSMessage(BaseModel):
    """WebSocket message wrapper"""
    type: WSMessageType = Field(..., description="Message type")
    room_id: str = Field(..., description="Room identifier")
    data: Dict[str, Any] = Field(..., description="Message payload")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    message_id: Optional[str] = Field(default_factory=lambda: str(uuid4()), description="Unique message ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "type": "message",
                "room_id": "room_123_456",
                "data": {
                    "message": "Hello!",
                    "sender_id": 123,
                    "sender_name": "John Doe"
                },
                "timestamp": "2024-01-15T10:30:00",
                "message_id": "msg_abc123"
            }
        }


class WSTypingIndicator(BaseModel):
    """Typing indicator message"""
    room_id: str
    user_id: int
    user_name: str
    status: TypingStatus
    
    class Config:
        json_schema_extra = {
            "example": {
                "room_id": "room_123_456",
                "user_id": 123,
                "user_name": "John Doe",
                "status": "typing"
            }
        }


class WSReadReceipt(BaseModel):
    """Read receipt message"""
    room_id: str
    message_id: int
    user_id: int
    user_name: str
    read_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "room_id": "room_123_456",
                "message_id": 789,
                "user_id": 123,
                "user_name": "John Doe",
                "read_at": "2024-01-15T10:30:00"
            }
        }


class WSReaction(BaseModel):
    """Reaction message"""
    room_id: str
    message_id: int
    user_id: int
    user_name: str
    emoji: str = Field(..., min_length=1, max_length=10)
    action: str = Field(..., pattern="^(add|remove)$", description="Add or remove reaction")
    
    class Config:
        json_schema_extra = {
            "example": {
                "room_id": "room_123_456",
                "message_id": 789,
                "user_id": 123,
                "user_name": "John Doe",
                "emoji": "👍",
                "action": "add"
            }
        }


class WSUserStatus(BaseModel):
    """User online/offline status"""
    user_id: int
    user_name: str
    status: str = Field(..., pattern="^(online|offline|away|busy)$")
    last_seen: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 123,
                "user_name": "John Doe",
                "status": "online",
                "last_seen": "2024-01-15T10:30:00"
            }
        }


# Action Schemas
class MarkAsRead(BaseModel):
    """Mark messages as read"""
    message_ids: List[int] = Field(..., min_length=1, description="Message IDs to mark as read")
    user_id: int = Field(..., description="User ID marking as read")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message_ids": [1, 2, 3, 4, 5],
                "user_id": 123
            }
        }


class AddReaction(BaseModel):
    """Add reaction to message"""
    message_id: int = Field(..., description="Message ID")
    emoji: str = Field(..., min_length=1, max_length=10, description="Emoji reaction")
    user_id: int = Field(..., description="User ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message_id": 789,
                "emoji": "👍",
                "user_id": 123
            }
        }


class RemoveReaction(BaseModel):
    """Remove reaction from message"""
    message_id: int = Field(..., description="Message ID")
    emoji: str = Field(..., min_length=1, max_length=10, description="Emoji to remove")
    user_id: int = Field(..., description="User ID")


class DeleteMessage(BaseModel):
    """Delete message"""
    message_id: int = Field(..., description="Message ID to delete")
    hard_delete: bool = Field(default=False, description="Permanently delete (vs soft delete)")
    delete_for_everyone: bool = Field(default=False, description="Delete for all participants")


class PinMessage(BaseModel):
    """Pin message in room"""
    message_id: int = Field(..., description="Message ID to pin")
    room_id: str = Field(..., description="Room ID")


class ForwardMessage(BaseModel):
    """Forward message to another room"""
    message_id: int = Field(..., description="Message ID to forward")
    target_room_ids: List[str] = Field(..., min_length=1, description="Target room IDs")


# Statistics Schemas
class ChatStats(BaseModel):
    """Chat statistics"""
    total_messages: int
    messages_today: int
    messages_this_week: int
    messages_this_month: int
    total_rooms: int
    active_rooms: int
    total_participants: int
    online_users: int
    messages_by_type: Dict[str, int]
    messages_by_room_type: Dict[str, int]
    most_active_rooms: List[Dict[str, Any]]
    most_active_users: List[Dict[str, Any]]
    peak_hours: List[int]
    average_response_time: Optional[float] = Field(None, description="Average response time in minutes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_messages": 50000,
                "messages_today": 500,
                "messages_this_week": 3500,
                "messages_this_month": 15000,
                "total_rooms": 200,
                "active_rooms": 150,
                "total_participants": 500,
                "online_users": 80,
                "messages_by_type": {
                    "text": 40000,
                    "image": 5000,
                    "file": 3000,
                    "audio": 2000
                },
                "messages_by_room_type": {
                    "direct": 30000,
                    "group": 15000,
                    "support": 5000
                },
                "most_active_rooms": [
                    {"room_id": "room_1", "room_name": "Emergency", "message_count": 1000}
                ],
                "most_active_users": [
                    {"user_id": 1, "user_name": "Dr. Smith", "message_count": 500}
                ],
                "peak_hours": [9, 10, 14, 15, 16],
                "average_response_time": 5.2
            }
        }


class RoomStats(BaseModel):
    """Statistics for a specific room"""
    room_id: str
    room_name: str
    total_messages: int
    total_participants: int
    active_participants: int
    messages_today: int
    messages_this_week: int
    first_message_at: Optional[datetime] = None
    last_message_at: Optional[datetime] = None
    most_active_user: Optional[Dict[str, Any]] = None
    message_types_breakdown: Dict[str, int]
    attachments_count: int
    average_messages_per_day: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "room_id": "room_123",
                "room_name": "General Discussion",
                "total_messages": 1500,
                "total_participants": 25,
                "active_participants": 18,
                "messages_today": 50,
                "messages_this_week": 300,
                "first_message_at": "2024-01-01T10:00:00",
                "last_message_at": "2024-01-15T16:30:00",
                "most_active_user": {
                    "user_id": 123,
                    "user_name": "John Doe",
                    "message_count": 200
                },
                "message_types_breakdown": {
                    "text": 1200,
                    "image": 200,
                    "file": 100
                },
                "attachments_count": 300,
                "average_messages_per_day": 100.0
            }
        }


# Search Schema
class ChatSearch(BaseModel):
    """Advanced chat search"""
    query: str = Field(..., min_length=1, description="Search query")
    room_ids: Optional[List[str]] = Field(None, description="Search in specific rooms")
    sender_ids: Optional[List[int]] = Field(None, description="Search messages from specific users")
    message_types: Optional[List[MessageType]] = Field(None, description="Filter by message types")
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    has_attachments: Optional[bool] = None
    limit: int = Field(50, ge=1, le=100)
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "prescription",
                "room_ids": ["room_123", "room_456"],
                "date_from": "2024-01-01T00:00:00",
                "limit": 50
            }
        }


class ChatSearchResult(BaseModel):
    """Search result item"""
    message: ChatResponse
    highlights: Optional[List[str]] = Field(None, description="Highlighted search matches")
    score: Optional[float] = Field(None, description="Relevance score")


class ChatSearchResults(BaseModel):
    """Search results"""
    total: int
    results: List[ChatSearchResult]
    query: str
    execution_time_ms: Optional[int] = None


# Notification Schema
class ChatNotification(BaseModel):
    """Chat notification"""
    notification_id: str = Field(default_factory=lambda: str(uuid4()))
    type: str = Field(..., description="Notification type (new_message, mention, etc.)")
    room_id: str
    room_name: str
    message: ChatResponse
    recipient_id: int
    title: str
    body: str
    priority: str = Field(default="normal", pattern="^(low|normal|high|urgent)$")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    is_read: bool = Field(default=False)
    
    class Config:
        json_schema_extra = {
            "example": {
                "notification_id": "notif_abc123",
                "type": "new_message",
                "room_id": "room_123",
                "room_name": "Dr. Smith",
                "recipient_id": 456,
                "title": "New message from Dr. Smith",
                "body": "Hello, how are you feeling today?",
                "priority": "normal",
                "timestamp": "2024-01-15T10:30:00",
                "is_read": False
            }
        }


# Export Schema
class ChatExport(BaseModel):
    """Export chat history"""
    room_id: str = Field(..., description="Room to export")
    format: str = Field(..., pattern="^(json|csv|pdf|txt)$", description="Export format")
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    include_attachments: bool = Field(default=False, description="Include attachment links")
    include_deleted: bool = Field(default=False, description="Include deleted messages")
    
    class Config:
        json_schema_extra = {
            "example": {
                "room_id": "room_123",
                "format": "pdf",
                "date_from": "2024-01-01T00:00:00",
                "date_to": "2024-01-31T23:59:59",
                "include_attachments": True,
                "include_deleted": False
            }
        }


# Bulk Operations
class ChatBulkDelete(BaseModel):
    """Bulk delete messages"""
    message_ids: List[int] = Field(..., min_length=1, max_length=100)
    hard_delete: bool = Field(default=False)
    
    @field_validator('message_ids')
    @classmethod
    def validate_message_ids(cls, v):
        if len(v) > 100:
            raise ValueError("Cannot delete more than 100 messages at once")
        return v


class ChatBulkMarkRead(BaseModel):
    """Bulk mark messages as read"""
    room_id: str = Field(..., description="Room ID")
    user_id: int = Field(..., description="User ID")
    up_to_message_id: Optional[int] = Field(None, description="Mark all messages up to this ID as read")
    mark_all: bool = Field(default=False, description="Mark all messages in room as read")