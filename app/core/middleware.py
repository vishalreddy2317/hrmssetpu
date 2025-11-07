"""
FastAPI Middleware for request/response processing
Includes logging, CORS, security headers, and request tracking
"""

from typing import Callable, Optional
from fastapi import Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import time
import uuid
import logging
from datetime import datetime

from .config import settings


# Configure logging
logger = logging.getLogger(__name__)


# ============================================
# Request ID Middleware
# ============================================

class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Add unique request ID to each request
    Useful for tracking and debugging
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate unique request ID
        request_id = str(uuid.uuid4())
        
        # Add to request state
        request.state.request_id = request_id
        
        # Process request
        response = await call_next(request)
        
        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id
        
        return response


# ============================================
# Request Logging Middleware
# ============================================

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Log all incoming requests and responses
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Start timer
        start_time = time.time()
        
        # Get request details
        method = request.method
        url = str(request.url)
        client_host = request.client.host if request.client else "unknown"
        request_id = getattr(request.state, "request_id", "N/A")
        
        # Log request
        logger.info(
            f"Request started",
            extra={
                "request_id": request_id,
                "method": method,
                "url": url,
                "client_host": client_host,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )
        
        # Process request
        try:
            response = await call_next(request)
            
            # Calculate processing time
            process_time = time.time() - start_time
            
            # Log response
            logger.info(
                f"Request completed",
                extra={
                    "request_id": request_id,
                    "method": method,
                    "url": url,
                    "status_code": response.status_code,
                    "process_time": f"{process_time:.3f}s",
                }
            )
            
            # Add processing time to response headers
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
            
        except Exception as e:
            # Log error
            process_time = time.time() - start_time
            logger.error(
                f"Request failed",
                extra={
                    "request_id": request_id,
                    "method": method,
                    "url": url,
                    "error": str(e),
                    "process_time": f"{process_time:.3f}s",
                },
                exc_info=True
            )
            raise


# ============================================
# Security Headers Middleware
# ============================================

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Add security headers to all responses
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        # Content Security Policy (adjust as needed)
        if settings.is_production:
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self' data:; "
                "connect-src 'self'; "
                "frame-ancestors 'none';"
            )
        
        # HSTS for production
        if settings.is_production:
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response


# ============================================
# Rate Limiting Middleware
# ============================================

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Simple rate limiting middleware
    For production, consider using Redis-based solution
    """
    
    def __init__(self, app: ASGIApp, calls: int = 100, period: int = 60):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.clients: dict = {}
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if not settings.rate_limit_enabled:
            return await call_next(request)
        
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        
        # Get current time
        now = time.time()
        
        # Clean old entries
        self.clients = {
            ip: timestamps
            for ip, timestamps in self.clients.items()
            if timestamps and timestamps[-1] > now - self.period
        }
        
        # Check rate limit
        if client_ip in self.clients:
            # Filter timestamps within period
            timestamps = [t for t in self.clients[client_ip] if t > now - self.period]
            
            if len(timestamps) >= self.calls:
                logger.warning(f"Rate limit exceeded for {client_ip}")
                return Response(
                    content="Rate limit exceeded",
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    headers={"Retry-After": str(self.period)}
                )
            
            timestamps.append(now)
            self.clients[client_ip] = timestamps
        else:
            self.clients[client_ip] = [now]
        
        return await call_next(request)


# ============================================
# Database Session Middleware
# ============================================

class DatabaseSessionMiddleware(BaseHTTPMiddleware):
    """
    Ensure database sessions are properly closed
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger.error(f"Database session error: {str(e)}")
            raise
        finally:
            # Cleanup is handled by dependency injection in get_db()
            pass


# ============================================
# Error Handler Middleware
# ============================================

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """
    Global error handler for unhandled exceptions
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            return await call_next(request)
        except Exception as e:
            request_id = getattr(request.state, "request_id", "N/A")
            
            logger.error(
                f"Unhandled exception",
                extra={
                    "request_id": request_id,
                    "error": str(e),
                    "path": request.url.path,
                },
                exc_info=True
            )
            
            # Return generic error response
            from fastapi.responses import JSONResponse
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "detail": "Internal server error",
                    "request_id": request_id,
                    "timestamp": datetime.utcnow().isoformat(),
                }
            )


# ============================================
# CORS Configuration
# ============================================

def get_cors_middleware() -> CORSMiddleware:
    """
    Configure CORS middleware
    """
    return CORSMiddleware(
        allow_origins=settings.cors.origins,
        allow_credentials=settings.cors.credentials,
        allow_methods=settings.cors.methods,
        allow_headers=settings.cors.headers,
        max_age=settings.cors.max_age,
    )


# ============================================
# Setup All Middleware
# ============================================

def setup_middleware(app):
    """
    Configure all middleware for the application
    
    Args:
        app: FastAPI application instance
    """
    
    # 1. CORS (must be first)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors.origins,
        allow_credentials=settings.cors.credentials,
        allow_methods=settings.cors.methods,
        allow_headers=settings.cors.headers,
        max_age=settings.cors.max_age,
    )
    
    # 2. Trusted Host (security)
    if settings.is_production:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["*"]  # Configure with actual domains in production
        )
    
    # 3. GZip Compression
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # 4. Request ID
    app.add_middleware(RequestIDMiddleware)
    
    # 5. Security Headers
    app.add_middleware(SecurityHeadersMiddleware)
    
    # 6. Request Logging
    if settings.debug or settings.is_development:
        app.add_middleware(RequestLoggingMiddleware)
    
    # 7. Rate Limiting
    if settings.rate_limit_enabled:
        app.add_middleware(
            RateLimitMiddleware,
            calls=settings.rate_limit_per_minute,
            period=60
        )
    
    # 8. Error Handler (should be last)
    app.add_middleware(ErrorHandlerMiddleware)
    
    logger.info("✅ All middleware configured successfully")


# ============================================
# Exports
# ============================================

__all__ = [
    "RequestIDMiddleware",
    "RequestLoggingMiddleware",
    "SecurityHeadersMiddleware",
    "RateLimitMiddleware",
    "DatabaseSessionMiddleware",
    "ErrorHandlerMiddleware",
    "setup_middleware",
]