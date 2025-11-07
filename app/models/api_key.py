"""
API Key Model
API authentication and access management
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, Index, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, validates
from typing import Optional

from .base import BaseModel


class APIKey(BaseModel):
    """
    API Key model
    """
    
    __tablename__ = "api_keys"
    
    # Key Details
    key: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    # Owner
    owner_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    owner_type: Mapped[str] = mapped_column(String(50), nullable=False, comment="user, application, integration")
    
    # Permissions
    permissions: Mapped[str] = mapped_column(Text, nullable=False, comment="JSON array of allowed endpoints/actions")
    
    # IP Whitelist
    ip_whitelist: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array of allowed IPs")
    
    # Rate Limiting
    rate_limit_per_minute: Mapped[int] = mapped_column(Integer, default=60)
    rate_limit_per_hour: Mapped[int] = mapped_column(Integer, default=1000)
    
    # Validity
    expires_at: Mapped[Optional[str]] = mapped_column(String(50), index=True)
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='active',
        nullable=False,
        index=True,
        comment="active, inactive, revoked, expired"
    )
    
    # Usage Stats
    total_requests: Mapped[int] = mapped_column(Integer, default=0)
    last_used_at: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Metadata
    metadata: Mapped[Optional[str]] = mapped_column(Text, comment="JSON additional data")
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('rate_limit_per_minute > 0', name='apikey_positive_rate_limit_minute'),
        CheckConstraint('rate_limit_per_hour > 0', name='apikey_positive_rate_limit_hour'),
        CheckConstraint('total_requests >= 0', name='apikey_positive_total_requests'),
        Index('idx_apikey_owner', 'owner_id', 'owner_type'),
        Index('idx_apikey_status', 'status', 'expires_at'),
        {'comment': 'API authentication and access management'}
    )
    
    # Validators
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['active', 'inactive', 'revoked', 'expired']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<APIKey(id={self.id}, name='{self.name}', status='{self.status}')>"