"""
✅ Auth Schemas - Pydantic v2 compatible
"""
from pydantic import BaseModel, EmailStr, validator, ConfigDict
from typing import Optional
from datetime import datetime


class UserRegistration(BaseModel):
    """Schema for user registration"""
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    username: Optional[str] = None
    password: str
    full_name: Optional[str] = None
    role: str = "user"
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    @validator('role')
    def validate_role(cls, v):
        allowed_roles = ['user', 'admin', 'doctor', 'nurse', 'patient', 'staff']
        if v not in allowed_roles:
            raise ValueError(f'Role must be one of: {", ".join(allowed_roles)}')
        return v
    
    @validator('phone')
    def validate_contact(cls, v, values):
        if v is None and values.get('email') is None:
            raise ValueError('Either email or phone must be provided')
        return v


class Login(BaseModel):
    """Schema for login"""
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: str
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    @validator('phone')
    def validate_contact(cls, v, values):
        if v is None and values.get('email') is None:
            raise ValueError('Either email or phone must be provided')
        return v


class VerifyOTP(BaseModel):
    """Schema for OTP verification"""
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    otp_code: str
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    @validator('phone')
    def validate_contact(cls, v, values):
        if v is None and values.get('email') is None:
            raise ValueError('Either email or phone must be provided')
        return v


class Token(BaseModel):
    """Schema for token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token payload data"""
    user_id: Optional[int] = None


class UserResponse(BaseModel):
    """
    ✅ SECURE - Never exposes password_hash
    """
    id: int
    email: Optional[str] = None
    phone: Optional[str] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    role: str
    is_verified: bool
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)