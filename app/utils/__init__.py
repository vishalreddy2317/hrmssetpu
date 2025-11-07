"""
✅ Utility functions and classes
Clean exports without duplicates
"""
from .security import (
    generate_api_key,
    generate_secure_token,
    generate_random_string,
    get_password_hash,
    verify_password
)
from .validators import (
    validate_email,
    validate_phone,
    validate_date_range,
    validate_username,
    validate_strong_password,
    sanitize_string,
    validate_file_extension
)
from .helpers import (
    setup_logger,
    format_date,
    parse_date,
    calculate_age,
    format_currency,
    paginate_data,
    truncate_string
)
from .email import EmailService, email_service
from .file_handlers import FileHandler

__all__ = [
    # Security
    'generate_api_key',
    'generate_secure_token',
    'generate_random_string',
    'get_password_hash',
    'verify_password',
    
    # Validators
    'validate_email',
    'validate_phone',
    'validate_date_range',
    'validate_username',
    'validate_strong_password',
    'sanitize_string',
    'validate_file_extension',
    
    # Helpers
    'setup_logger',
    'format_date',
    'parse_date',
    'calculate_age',
    'format_currency',
    'paginate_data',
    'truncate_string',
    
    # Email
    'EmailService',
    'email_service',
    
    # File handlers
    'FileHandler',
]