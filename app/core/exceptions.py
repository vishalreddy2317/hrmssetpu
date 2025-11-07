"""
Custom exceptions for the Hospital Management System
"""

from typing import Any, Optional, Dict
from fastapi import HTTPException, status


# ============================================
# Base Custom Exception
# ============================================

class BaseHTTPException(HTTPException):
    """Base exception class with additional fields"""
    
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs: Any
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_code = error_code
        self.extra_data = kwargs


# ============================================
# Authentication & Authorization Exceptions
# ============================================

class UnauthorizedException(BaseHTTPException):
    """Raised when authentication fails"""
    
    def __init__(
        self,
        detail: str = "Authentication required",
        error_code: str = "UNAUTHORIZED",
        **kwargs
    ):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code=error_code,
            headers={"WWW-Authenticate": "Bearer"},
            **kwargs
        )


class ForbiddenException(BaseHTTPException):
    """Raised when user doesn't have permission"""
    
    def __init__(
        self,
        detail: str = "Permission denied",
        error_code: str = "FORBIDDEN",
        **kwargs
    ):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code=error_code,
            **kwargs
        )


class InvalidCredentialsException(BaseHTTPException):
    """Raised when credentials are invalid"""
    
    def __init__(
        self,
        detail: str = "Invalid credentials",
        error_code: str = "INVALID_CREDENTIALS",
        **kwargs
    ):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code=error_code,
            **kwargs
        )


class TokenExpiredException(BaseHTTPException):
    """Raised when JWT token has expired"""
    
    def __init__(
        self,
        detail: str = "Token has expired",
        error_code: str = "TOKEN_EXPIRED",
        **kwargs
    ):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code=error_code,
            **kwargs
        )


class InvalidTokenException(BaseHTTPException):
    """Raised when JWT token is invalid"""
    
    def __init__(
        self,
        detail: str = "Invalid token",
        error_code: str = "INVALID_TOKEN",
        **kwargs
    ):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code=error_code,
            **kwargs
        )


# ============================================
# Resource Exceptions
# ============================================

class NotFoundException(BaseHTTPException):
    """Raised when resource is not found"""
    
    def __init__(
        self,
        detail: str = "Resource not found",
        error_code: str = "NOT_FOUND",
        resource: Optional[str] = None,
        resource_id: Optional[Any] = None,
        **kwargs
    ):
        if resource and resource_id:
            detail = f"{resource} with ID {resource_id} not found"
        
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code=error_code,
            resource=resource,
            resource_id=resource_id,
            **kwargs
        )


class AlreadyExistsException(BaseHTTPException):
    """Raised when trying to create duplicate resource"""
    
    def __init__(
        self,
        detail: str = "Resource already exists",
        error_code: str = "ALREADY_EXISTS",
        resource: Optional[str] = None,
        **kwargs
    ):
        if resource:
            detail = f"{resource} already exists"
        
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            error_code=error_code,
            resource=resource,
            **kwargs
        )


class ConflictException(BaseHTTPException):
    """Raised when there's a conflict with current state"""
    
    def __init__(
        self,
        detail: str = "Conflict with current state",
        error_code: str = "CONFLICT",
        **kwargs
    ):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            error_code=error_code,
            **kwargs
        )


# ============================================
# Validation Exceptions
# ============================================

class BadRequestException(BaseHTTPException):
    """Raised when request data is invalid"""
    
    def __init__(
        self,
        detail: str = "Bad request",
        error_code: str = "BAD_REQUEST",
        **kwargs
    ):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code=error_code,
            **kwargs
        )


class ValidationException(BaseHTTPException):
    """Raised when validation fails"""
    
    def __init__(
        self,
        detail: str = "Validation error",
        error_code: str = "VALIDATION_ERROR",
        errors: Optional[list] = None,
        **kwargs
    ):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code=error_code,
            errors=errors,
            **kwargs
        )


# ============================================
# Business Logic Exceptions
# ============================================

class BusinessLogicException(BaseHTTPException):
    """Raised when business logic validation fails"""
    
    def __init__(
        self,
        detail: str = "Business logic error",
        error_code: str = "BUSINESS_LOGIC_ERROR",
        **kwargs
    ):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code=error_code,
            **kwargs
        )


class InsufficientResourcesException(BaseHTTPException):
    """Raised when there are insufficient resources"""
    
    def __init__(
        self,
        detail: str = "Insufficient resources",
        error_code: str = "INSUFFICIENT_RESOURCES",
        **kwargs
    ):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code=error_code,
            **kwargs
        )


# ============================================
# Rate Limiting & Quota Exceptions
# ============================================

class RateLimitExceededException(BaseHTTPException):
    """Raised when rate limit is exceeded"""
    
    def __init__(
        self,
        detail: str = "Rate limit exceeded",
        error_code: str = "RATE_LIMIT_EXCEEDED",
        retry_after: Optional[int] = None,
        **kwargs
    ):
        headers = {"Retry-After": str(retry_after)} if retry_after else None
        
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail,
            error_code=error_code,
            headers=headers,
            **kwargs
        )


# ============================================
# Server Exceptions
# ============================================

class InternalServerException(BaseHTTPException):
    """Raised when internal server error occurs"""
    
    def __init__(
        self,
        detail: str = "Internal server error",
        error_code: str = "INTERNAL_SERVER_ERROR",
        **kwargs
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code=error_code,
            **kwargs
        )


class ServiceUnavailableException(BaseHTTPException):
    """Raised when service is temporarily unavailable"""
    
    def __init__(
        self,
        detail: str = "Service temporarily unavailable",
        error_code: str = "SERVICE_UNAVAILABLE",
        **kwargs
    ):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail,
            error_code=error_code,
            **kwargs
        )


# ============================================
# Database Exceptions
# ============================================

class DatabaseException(BaseHTTPException):
    """Raised when database operation fails"""
    
    def __init__(
        self,
        detail: str = "Database operation failed",
        error_code: str = "DATABASE_ERROR",
        **kwargs
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code=error_code,
            **kwargs
        )


# ============================================
# Hospital-Specific Exceptions
# ============================================

class FloorNotFoundException(NotFoundException):
    """Raised when floor is not found"""
    
    def __init__(self, floor_id: int):
        super().__init__(
            resource="Floor",
            resource_id=floor_id,
            error_code="FLOOR_NOT_FOUND"
        )


class RoomNotFoundException(NotFoundException):
    """Raised when room is not found"""
    
    def __init__(self, room_id: int):
        super().__init__(
            resource="Room",
            resource_id=room_id,
            error_code="ROOM_NOT_FOUND"
        )


class PatientNotFoundException(NotFoundException):
    """Raised when patient is not found"""
    
    def __init__(self, patient_id: int):
        super().__init__(
            resource="Patient",
            resource_id=patient_id,
            error_code="PATIENT_NOT_FOUND"
        )


class BedNotAvailableException(BusinessLogicException):
    """Raised when bed is not available"""
    
    def __init__(self):
        super().__init__(
            detail="No beds available",
            error_code="BED_NOT_AVAILABLE"
        )


class AppointmentConflictException(ConflictException):
    """Raised when appointment time conflicts"""
    
    def __init__(self):
        super().__init__(
            detail="Appointment time conflicts with existing appointment",
            error_code="APPOINTMENT_CONFLICT"
        )


# ============================================
# Exports
# ============================================

__all__ = [
    "BaseHTTPException",
    "UnauthorizedException",
    "ForbiddenException",
    "InvalidCredentialsException",
    "TokenExpiredException",
    "InvalidTokenException",
    "NotFoundException",
    "AlreadyExistsException",
    "ConflictException",
    "BadRequestException",
    "ValidationException",
    "BusinessLogicException",
    "InsufficientResourcesException",
    "RateLimitExceededException",
    "InternalServerException",
    "ServiceUnavailableException",
    "DatabaseException",
    "FloorNotFoundException",
    "RoomNotFoundException",
    "PatientNotFoundException",
    "BedNotAvailableException",
    "AppointmentConflictException",
]
