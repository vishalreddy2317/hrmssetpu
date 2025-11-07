"""
Custom validators for schemas
"""

import re
from datetime import datetime
from typing import Optional


def validate_phone_number(phone: str) -> bool:
    """Validate phone number format"""
    pattern = r'^\+?1?\d{9,15}$'
    return bool(re.match(pattern, phone.replace('-', '').replace(' ', '')))


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))


def validate_date_format(date_str: str, format: str = "%Y-%m-%d") -> bool:
    """Validate date string format"""
    try:
        datetime.strptime(date_str, format)
        return True
    except ValueError:
        return False


def validate_time_format(time_str: str, format: str = "%H:%M") -> bool:
    """Validate time string format"""
    try:
        datetime.strptime(time_str, format)
        return True
    except ValueError:
        return False


def validate_pincode(pincode: str, country: str = "IN") -> bool:
    """Validate pincode/zipcode based on country"""
    patterns = {
        "IN": r'^\d{6}$',  # India: 6 digits
        "US": r'^\d{5}(-\d{4})?$',  # USA: 5 or 9 digits
        "UK": r'^[A-Z]{1,2}\d{1,2}[A-Z]?\s?\d[A-Z]{2}$',  # UK postcode
    }
    pattern = patterns.get(country, r'^\d{4,10}$')  # Default: 4-10 digits
    return bool(re.match(pattern, pincode.upper()))


def validate_aadhar(aadhar: str) -> bool:
    """Validate Aadhar number (India)"""
    pattern = r'^\d{12}$'
    return bool(re.match(pattern, aadhar.replace(' ', '')))


def validate_pan(pan: str) -> bool:
    """Validate PAN number (India)"""
    pattern = r'^[A-Z]{5}\d{4}[A-Z]$'
    return bool(re.match(pattern, pan.upper()))


def validate_age(age: int, min_age: int = 0, max_age: int = 150) -> bool:
    """Validate age range"""
    return min_age <= age <= max_age


def validate_percentage(value: float, min_val: float = 0, max_val: float = 100) -> bool:
    """Validate percentage value"""
    return min_val <= value <= max_val