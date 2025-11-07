"""
Chat Model
Real-time chat messaging
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, Index
from sqlalchemy.orm import Mapped, mapped_column, validates
from typing import Optional

from .base import BaseModel


class Chat(BaseModel):
    """
    Real-time chat model
    """
    
    __tablename__ = "chats"
    
    # Room/Channel
    room_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    room_name: Mapped[Optional[str]] = mapped_column(String(200))
    room_type: Mapped[str] = mapped_column(
        String(20),
        default='direct',
        nullable=False,
        comment="direct, group, support, emergency"
    )
    
    # Sender
    sender_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    sender_name: Mapped[str] = mapped_column(String(200), nullable=False)
    sender_type: Mapped[str] = mapped_column(String(20))
    
    # Message
    message: Mapped[str] = mapped_column(Text, nullable=False)
    message_type: Mapped[str] = mapped_column(
        String(20),
        default='text',
        nullable=False,
        comment="text, image, file, audio, video, location"
    )
    
    # Attachments
    attachment_url: Mapped[Optional[str]] = mapped_column(String(500))
    attachment_type: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Status
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    read_by: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array of user IDs who read")
    
    # Reply To
    reply_to_message_id: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Reactions
    reactions: Mapped[Optional[str]] = mapped_column(Text, comment="JSON object of reactions")
    
    # Edit
    is_edited: Mapped[bool] = mapped_column(Boolean, default=False)
    edited_at: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Delete
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Table Arguments
    __table_args__ = (
        Index('idx_chat_room', 'room_id', 'created_at'),
        Index('idx_chat_sender', 'sender_id', 'created_at'),
        {'comment': 'Real-time chat messaging'}
    )
    
    # Validators
    @validates('room_type')
    def validate_room_type(self, key, value):
        valid_types = ['direct', 'group', 'support', 'emergency', 'announcement']
        if value.lower() not in valid_types:
            raise ValueError(f"Room type must be one of: {', '.join(valid_types)}")
        return value.lower()
    
    @validates('message_type')
    def validate_message_type(self, key, value):
        valid_types = ['text', 'image', 'file', 'audio', 'video', 'location']
        if value.lower() not in valid_types:
            raise ValueError(f"Message type must be one of: {', '.join(valid_types)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<Chat(id={self.id}, room='{self.room_id}', sender='{self.sender_name}')>"