"""
Security utilities for authentication and authorization
Includes JWT, password hashing, and token management
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
import secrets
import string

from .config import settings


# ============================================
# Password Hashing Context
# ============================================

# Argon2 (recommended for production)
pwd_context_argon2 = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__memory_cost=65536,
    argon2__time_cost=3,
    argon2__parallelism=4,
)

# Bcrypt (alternative)
pwd_context_bcrypt = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=settings.security.password_bcrypt_rounds,
)

# Select password context based on settings
pwd_context = (
    pwd_context_argon2
    if settings.security.password_hash_algorithm == "argon2"
    else pwd_context_bcrypt
)


# ============================================
# Password Functions
# ============================================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against hashed password
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password from database
        
    Returns:
        True if password matches, False otherwise
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """
    Hash a password for storing
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password string
    """
    return pwd_context.hash(password)


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password strength based on requirements
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(password) < settings.security.password_min_length:
        return False, f"Password must be at least {settings.security.password_min_length} characters"
    
    if settings.security.password_require_uppercase and not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    
    if settings.security.password_require_lowercase and not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    
    if settings.security.password_require_digit and not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit"
    
    if settings.security.password_require_special:
        special_chars = set(string.punctuation)
        if not any(c in special_chars for c in password):
            return False, "Password must contain at least one special character"
    
    return True, "Password is strong"


def generate_random_password(length: int = 12) -> str:
    """
    Generate a random secure password
    
    Args:
        length: Password length (default: 12)
        
    Returns:
        Random password string
    """
    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        is_valid, _ = validate_password_strength(password)
        if is_valid:
            return password


# ============================================
# JWT Token Functions
# ============================================

def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT access token
    
    Args:
        data: Data to encode in token (usually user_id, email)
        expires_delta: Custom expiration time
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.security.access_token_expire_minutes
        )
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access",
    })
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.security.secret_key,
        algorithm=settings.security.algorithm
    )
    
    return encoded_jwt


def create_refresh_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT refresh token
    
    Args:
        data: Data to encode in token
        expires_delta: Custom expiration time
        
    Returns:
        Encoded JWT refresh token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            days=settings.security.refresh_token_expire_days
        )
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh",
    })
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.security.secret_key,
        algorithm=settings.security.algorithm
    )
    
    return encoded_jwt


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and validate JWT token
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded token payload or None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.security.secret_key,
            algorithms=[settings.security.algorithm]
        )
        return payload
    except JWTError:
        return None


def verify_token(token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
    """
    Verify token and check type
    
    Args:
        token: JWT token string
        token_type: Expected token type ('access' or 'refresh')
        
    Returns:
        Decoded payload if valid, None otherwise
    """
    payload = decode_token(token)
    
    if not payload:
        return None
    
    if payload.get("type") != token_type:
        return None
    
    return payload


# ============================================
# API Key Functions
# ============================================

def generate_api_key(length: int = 32) -> str:
    """
    Generate a random API key
    
    Args:
        length: API key length
        
    Returns:
        Random API key string
    """
    return secrets.token_urlsafe(length)


def verify_api_key(api_key: str, stored_hash: str) -> bool:
    """
    Verify API key against stored hash
    
    Args:
        api_key: Plain API key
        stored_hash: Hashed API key from database
        
    Returns:
        True if valid, False otherwise
    """
    return pwd_context.verify(api_key, stored_hash)


def hash_api_key(api_key: str) -> str:
    """
    Hash an API key for storage
    
    Args:
        api_key: Plain API key
        
    Returns:
        Hashed API key
    """
    return get_password_hash(api_key)


# ============================================
# Token Utilities
# ============================================

def create_reset_password_token(user_id: int, email: str) -> str:
    """
    Create password reset token
    
    Args:
        user_id: User ID
        email: User email
        
    Returns:
        Password reset token
    """
    data = {
        "sub": str(user_id),
        "email": email,
        "type": "reset_password",
    }
    
    expires_delta = timedelta(hours=24)  # 24 hours validity
    return create_access_token(data, expires_delta)


def create_email_verification_token(user_id: int, email: str) -> str:
    """
    Create email verification token
    
    Args:
        user_id: User ID
        email: User email
        
    Returns:
        Email verification token
    """
    data = {
        "sub": str(user_id),
        "email": email,
        "type": "email_verification",
    }
    
    expires_delta = timedelta(hours=48)  # 48 hours validity
    return create_access_token(data, expires_delta)


# ============================================
# Exports
# ============================================

__all__ = [
    "verify_password",
    "get_password_hash",
    "validate_password_strength",
    "generate_random_password",
    "create_access_token",
    "create_refresh_token",
    "decode_token",
    "verify_token",
    "generate_api_key",
    "verify_api_key",
    "hash_api_key",
    "create_reset_password_token",
    "create_email_verification_token",
]