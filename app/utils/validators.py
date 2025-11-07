"""
✅ Data validation utilities
"""
import re
from typing import Any, Dict
from datetime import datetime, date


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """
    Validate phone number format
    Accepts: +1234567890, 1234567890, +12-345-67890
    """
    # Remove common separators
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    # Check if it's a valid international format
    pattern = r'^\+?[1-9]\d{1,14}$'
    return bool(re.match(pattern, cleaned))


def validate_date_range(start_date: date, end_date: date) -> bool:
    """Validate that start date is before or equal to end date"""
    return start_date <= end_date


def sanitize_string(value: str) -> str:
    """
    Sanitize string by removing extra whitespace
    and potential XSS characters
    """
    # Remove extra whitespace
    cleaned = ' '.join(value.strip().split())
    # Basic XSS prevention (remove HTML tags)
    cleaned = re.sub(r'<[^>]+>', '', cleaned)
    return cleaned


def validate_file_extension(filename: str, allowed_extensions: list) -> bool:
    """Validate file extension"""
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in allowed_extensions


def validate_username(username: str) -> bool:
    """
    Validate username format
    Rules: 3-20 chars, alphanumeric, underscore, hyphen
    """
    pattern = r'^[a-zA-Z0-9_-]{3,20}$'
    return bool(re.match(pattern, username))


def validate_strong_password(password: str) -> tuple[bool, str]:
    """
    Validate password strength
    Returns: (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, "Password is strong"