"""
Audit Log Model
System audit trail and activity logging
"""

from sqlalchemy import Column, Integer, String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column, validates
from typing import Optional

from .base import BaseModel


class AuditLog(BaseModel):
    """
    Audit log model for tracking all system actions
    """
    
    __tablename__ = "audit_logs"
    
    # User/Actor
    user_id: Mapped[Optional[int]] = mapped_column(Integer, index=True)
    username: Mapped[Optional[str]] = mapped_column(String(200))
    user_type: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Action
    action: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        comment="create, update, delete, login, logout, view, export, approve"
    )
    
    # Resource
    resource_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    resource_id: Mapped[Optional[int]] = mapped_column(Integer, index=True)
    resource_name: Mapped[Optional[str]] = mapped_column(String(200))
    
    # Details
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Changes (before/after)
    old_values: Mapped[Optional[str]] = mapped_column(Text, comment="JSON of old values")
    new_values: Mapped[Optional[str]] = mapped_column(Text, comment="JSON of new values")
    
    # Request Details
    ip_address: Mapped[Optional[str]] = mapped_column(String(50))
    user_agent: Mapped[Optional[str]] = mapped_column(String(500))
    request_method: Mapped[Optional[str]] = mapped_column(String(10))
    request_path: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='success',
        nullable=False,
        comment="success, failure, error"
    )
    
    # Error Details (if any)
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    
    # Timestamp (inherited from BaseModel, but we index it)
    
    # Table Arguments
    __table_args__ = (
        Index('idx_auditlog_user', 'user_id', 'created_at'),
        Index('idx_auditlog_resource', 'resource_type', 'resource_id'),
        Index('idx_auditlog_action', 'action', 'created_at'),
        Index('idx_auditlog_timestamp', 'created_at'),
        {'comment': 'System audit trail and activity logging'}
    )
    
    # Validators
    @validates('action')
    def validate_action(self, key, value):
        valid_actions = [
            'create', 'update', 'delete', 'login', 'logout',
            'view', 'export', 'approve', 'reject', 'send'
        ]
        if value.lower() not in valid_actions:
            raise ValueError(f"Action must be one of: {', '.join(valid_actions)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['success', 'failure', 'error']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<AuditLog(id={self.id}, action='{self.action}', resource='{self.resource_type}')>"