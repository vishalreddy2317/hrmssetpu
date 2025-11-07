"""
Core module for Hospital Management System
Includes configuration, database, security, and utilities
"""

from .config import settings
from .database import Base, get_db, engine
from .security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    get_password_hash,
)
from .exceptions import (
    NotFoundException,
    BadRequestException,
    UnauthorizedException,
    ForbiddenException,
)

__all__ = [
    # Settings
    "settings",
    
    # Database
    "Base",
    "get_db",
    "engine",
    
    # Security
    "create_access_token",
    "create_refresh_token",
    "verify_password",
    "get_password_hash",
    
    # Exceptions
    "NotFoundException",
    "BadRequestException",
    "UnauthorizedException",
    "ForbiddenException",
]

__version__ = "1.0.0"