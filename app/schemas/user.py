"""
User Schemas - Pydantic V2
Authentication and user management
"""

from typing import Optional
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from datetime import datetime
import re

from .base import BaseSchema, BaseResponseSchema


# ============================================
# User Create
# ============================================

class UserCreate(BaseSchema):
    """Schema for creating new user"""
    
    username: str = Field(..., min_length=3, max_length=100, description="Unique username")
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, max_length=128, description="User password")
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    phone: Optional[str] = Field(default=None, max_length=20)
    user_type: str = Field(..., description="admin, doctor, nurse, patient, staff")
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v
    
    @field_validator('user_type')
    @classmethod
    def validate_user_type(cls, v: str) -> str:
        """Validate user type"""
        allowed = ['admin', 'doctor', 'nurse', 'patient', 'staff', 'pharmacist', 'technician']
        if v.lower() not in allowed:
            raise ValueError(f'User type must be one of: {", ".join(allowed)}')
        return v.lower()
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        """Validate username format"""
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Username can only contain letters, numbers, underscores, and hyphens')
        return v.lower()


# ============================================
# User Update
# ============================================

class UserUpdate(BaseSchema):
    """Schema for updating user"""
    
    first_name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    last_name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    phone: Optional[str] = Field(default=None, max_length=20)
    profile_image: Optional[str] = Field(default=None, max_length=500)
    bio: Optional[str] = Field(default=None, max_length=1000)
    is_active: Optional[bool] = None


class UserPasswordChange(BaseSchema):
    """Schema for changing password"""
    
    current_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str = Field(..., min_length=8, max_length=128)
    
    @field_validator('new_password')
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        """Validate new password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one digit')
        return v


# ============================================
# User Response
# ============================================

class UserResponse(BaseResponseSchema):
    """Schema for user response"""
    
    username: str
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    user_type: str
    role_id: Optional[int] = None
    is_verified: bool
    is_superuser: bool
    profile_image: Optional[str] = None
    last_login_at: Optional[datetime] = None
    
    @property
    def full_name(self) -> str:
        """Get full name"""
        return f"{self.first_name} {self.last_name}"


class UserListResponse(BaseSchema):
    """Schema for user list response"""
    
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    user_type: str
    is_active: bool
    is_verified: bool
    created_at: datetime


# ============================================
# Authentication
# ============================================

class UserLogin(BaseSchema):
    """Schema for user login"""
    
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=8)
    remember_me: bool = Field(default=False)


class TokenResponse(BaseSchema):
    """Schema for token response"""
    
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class TokenRefresh(BaseSchema):
    """Schema for token refresh"""
    
    refresh_token: str = Field(..., description="Refresh token")


class PasswordResetRequest(BaseSchema):
    """Schema for password reset request"""
    
    email: EmailStr = Field(..., description="Email address")


class PasswordReset(BaseSchema):
    """Schema for password reset"""
    
    token: str = Field(..., description="Reset token")
    new_password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str = Field(..., min_length=8, max_length=128)
    
    @field_validator('new_password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one digit')
        return v


class EmailVerification(BaseSchema):
    """Schema for email verification"""
    
    token: str = Field(..., description="Verification token")


# ============================================
# Exports
# ============================================

__all__ = [
    "UserCreate",
    "UserUpdate",
    "UserPasswordChange",
    "UserResponse",
    "UserListResponse",
    "UserLogin",
    "TokenResponse",
    "TokenRefresh",
    "PasswordResetRequest",
    "PasswordReset",
    "EmailVerification",
]