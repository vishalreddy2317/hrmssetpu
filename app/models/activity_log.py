"""
Activity Log Model
User activity tracking (lightweight version of audit log)
"""

from sqlalchemy import Column, Integer, String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column, validates
from typing import Optional

from .base import BaseModel


class ActivityLog(BaseModel):
    """
    User activity log model
    """
    
    __tablename__ = "activity_logs"
    
    # User
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    user_name: Mapped[str] = mapped_column(String(200), nullable=False)
    user_type: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Activity
    activity_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        comment="login, logout, page_view, action, download, upload"
    )
    
    # Description
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    
    # Metadata
    metadata: Mapped[Optional[str]] = mapped_column(Text, comment="JSON additional info")
    
    # Session
    session_id: Mapped[Optional[str]] = mapped_column(String(100), index=True)
    
    # Device Info
    ip_address: Mapped[Optional[str]] = mapped_column(String(50))
    device_type: Mapped[Optional[str]] = mapped_column(String(50), comment="desktop, mobile, tablet")
    browser: Mapped[Optional[str]] = mapped_column(String(100))
    os: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Location
    country: Mapped[Optional[str]] = mapped_column(String(100))
    city: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Duration (for sessions)
    duration_seconds: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Table Arguments
    __table_args__ = (
        Index('idx_activitylog_user', 'user_id', 'created_at'),
        Index('idx_activitylog_type', 'activity_type', 'created_at'),
        Index('idx_activitylog_session', 'session_id'),
        {'comment': 'User activity tracking'}
    )
    
    # Validators
    @validates('activity_type')
    def validate_activity_type(self, key, value):
        valid_types = [
            'login', 'logout', 'page_view', 'action',
            'download', 'upload', 'search', 'export'
        ]
        if value.lower() not in valid_types:
            raise ValueError(f"Activity type must be one of: {', '.join(valid_types)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<ActivityLog(id={self.id}, user='{self.user_name}', activity='{self.activity_type}')>"