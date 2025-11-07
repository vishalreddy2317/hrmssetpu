"""
Auth module - handles authentication and authorization
"""
from .models import User, OTPCode
from .schemas import UserRegistration, Login, VerifyOTP, Token, UserResponse
from .utils import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token
)

__all__ = [
    'User',
    'OTPCode',
    'UserRegistration',
    'Login',
    'VerifyOTP',
    'Token',
    'UserResponse',
    'hash_password',
    'verify_password',
    'create_access_token',
    'create_refresh_token',
    'verify_token',
]