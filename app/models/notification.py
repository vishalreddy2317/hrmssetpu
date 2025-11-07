"""
Notification Model
System notifications and alerts
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, validates
from typing import Optional

from .base import BaseModel


class Notification(BaseModel):
    """
    Notification model
    """
    
    __tablename__ = "notifications"
    
    # Notification Details
    title: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Type
    notification_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        comment="info, warning, error, success, reminder, alert"
    )
    
    # Category
    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="appointment, payment, test_result, prescription, general, emergency"
    )
    
    # Recipient
    user_id: Mapped[Optional[int]] = mapped_column(Integer, index=True)
    recipient_email: Mapped[Optional[str]] = mapped_column(String(100))
    recipient_phone: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Recipient Type
    recipient_type: Mapped[Optional[str]] = mapped_column(String(20), comment="patient, doctor, nurse, staff")
    
    # Delivery Channels
    send_email: Mapped[bool] = mapped_column(Boolean, default=True)
    send_sms: Mapped[bool] = mapped_column(Boolean, default=False)
    send_push: Mapped[bool] = mapped_column(Boolean, default=True)
    send_in_app: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Status
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    read_at: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Sent Status
    email_sent: Mapped[bool] = mapped_column(Boolean, default=False)
    sms_sent: Mapped[bool] = mapped_column(Boolean, default=False)
    push_sent: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Priority
    priority: Mapped[str] = mapped_column(
        String(20),
        default='normal',
        nullable=False,
        comment="low, normal, high, urgent"
    )
    
    # Action
    action_url: Mapped[Optional[str]] = mapped_column(String(500))
    action_text: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Reference
    reference_type: Mapped[Optional[str]] = mapped_column(String(50))
    reference_id: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Expiry
    expires_at: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Table Arguments
    __table_args__ = (
        Index('idx_notification_user', 'user_id', 'is_read'),
        Index('idx_notification_type', 'notification_type', 'priority'),
        Index('idx_notification_created', 'created_at', 'is_read'),
        {'comment': 'System notifications and alerts'}
    )
    
    # Validators
    @validates('notification_type')
    def validate_notification_type(self, key, value):
        valid_types = ['info', 'warning', 'error', 'success', 'reminder', 'alert']
        if value.lower() not in valid_types:
            raise ValueError(f"Notification type must be one of: {', '.join(valid_types)}")
        return value.lower()
    
    @validates('priority')
    def validate_priority(self, key, value):
        valid_priorities = ['low', 'normal', 'high', 'urgent']
        if value.lower() not in valid_priorities:
            raise ValueError(f"Priority must be one of: {', '.join(valid_priorities)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<Notification(id={self.id}, title='{self.title}', type='{self.notification_type}')>"