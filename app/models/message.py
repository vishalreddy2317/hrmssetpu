"""
Message Model
Internal messaging system
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional

from .base import BaseModel


class Message(BaseModel):
    """
    Internal message model
    """
    
    __tablename__ = "messages"
    
    # Message Details
    subject: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Sender
    sender_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    sender_name: Mapped[str] = mapped_column(String(200), nullable=False)
    sender_type: Mapped[str] = mapped_column(String(20), comment="patient, doctor, nurse, staff, admin")
    
    # Recipient
    recipient_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    recipient_name: Mapped[str] = mapped_column(String(200), nullable=False)
    recipient_type: Mapped[str] = mapped_column(String(20))
    
    # Message Type
    message_type: Mapped[str] = mapped_column(
        String(50),
        default='direct',
        nullable=False,
        comment="direct, broadcast, announcement, reply"
    )
    
    # Thread (for replies)
    parent_message_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("messages.id", ondelete="CASCADE"),
        index=True
    )
    thread_id: Mapped[Optional[str]] = mapped_column(String(50), index=True)
    
    # Status
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    read_at: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Flags
    is_starred: Mapped[bool] = mapped_column(Boolean, default=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)
    is_draft: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Priority
    priority: Mapped[str] = mapped_column(
        String(20),
        default='normal',
        nullable=False,
        comment="low, normal, high, urgent"
    )
    
    # Attachments
    attachments: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array of attachment URLs")
    
    # Deletion
    deleted_by_sender: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_by_recipient: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Relationships
    parent_message: Mapped[Optional["Message"]] = relationship(
        "Message",
        remote_side="Message.id",
        backref="replies"
    )
    
    # Table Arguments
    __table_args__ = (
        Index('idx_message_sender', 'sender_id', 'created_at'),
        Index('idx_message_recipient', 'recipient_id', 'is_read'),
        Index('idx_message_thread', 'thread_id', 'created_at'),
        {'comment': 'Internal messaging system'}
    )
    
    # Validators
    @validates('message_type')
    def validate_message_type(self, key, value):
        valid_types = ['direct', 'broadcast', 'announcement', 'reply']
        if value.lower() not in valid_types:
            raise ValueError(f"Message type must be one of: {', '.join(valid_types)}")
        return value.lower()
    
    @validates('priority')
    def validate_priority(self, key, value):
        valid_priorities = ['low', 'normal', 'high', 'urgent']
        if value.lower() not in valid_priorities:
            raise ValueError(f"Priority must be one of: {', '.join(valid_priorities)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<Message(id={self.id}, subject='{self.subject}', from='{self.sender_name}')>"