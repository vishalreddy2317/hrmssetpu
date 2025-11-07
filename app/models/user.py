"""
User Model
Authentication and user management
"""

from sqlalchemy import Column, Integer, String, Boolean, Index, Text
from sqlalchemy.orm import Mapped, mapped_column, validates
from typing import Optional
import re

from .base import BaseModel


class User(BaseModel):
    """
    User authentication model
    """
    
    __tablename__ = "users"
    
    # Basic Info
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    
    # Password (hashed)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Personal Info
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    
    # User Type
    user_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
        comment="admin, doctor, nurse, patient, staff"
    )
    
    # Role
    role_id: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Status
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Email Verification
    email_verified_at: Mapped[Optional[str]] = mapped_column(String(50))
    verification_token: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Password Reset
    reset_token: Mapped[Optional[str]] = mapped_column(String(255))
    reset_token_expires: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Last Login
    last_login_at: Mapped[Optional[str]] = mapped_column(String(50))
    last_login_ip: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Security
    failed_login_attempts: Mapped[int] = mapped_column(Integer, default=0)
    locked_until: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Two-Factor Authentication
    two_factor_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    two_factor_secret: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Profile
    profile_image: Mapped[Optional[str]] = mapped_column(String(500))
    bio: Mapped[Optional[str]] = mapped_column(Text)
    
    # Preferences
    preferences: Mapped[Optional[str]] = mapped_column(Text, comment="JSON user preferences")
    
    # Table Arguments
    __table_args__ = (
        Index('idx_user_type', 'user_type', 'is_active'),
        Index('idx_user_email_verified', 'email', 'is_verified'),
        {'comment': 'User authentication and management'}
    )
    
    # Validators
    @validates('email')
    def validate_email(self, key, value):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise ValueError("Invalid email format")
        return value.lower()
    
    @validates('user_type')
    def validate_user_type(self, key, value):
        valid_types = ['admin', 'doctor', 'nurse', 'patient', 'staff', 'pharmacist', 'technician']
        if value.lower() not in valid_types:
            raise ValueError(f"User type must be one of: {', '.join(valid_types)}")
        return value.lower()
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', type='{self.user_type}')>"