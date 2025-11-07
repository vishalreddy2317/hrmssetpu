"""
✅ Additional security utilities
Functions that don't belong in auth module
"""
from passlib.context import CryptContext
import secrets

# Password context (can be used independently)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def generate_api_key() -> str:
    """Generate a random API key"""
    return secrets.token_urlsafe(32)


def generate_secure_token(length: int = 32) -> str:
    """Generate a secure random token"""
    return secrets.token_hex(length)


def generate_random_string(length: int = 16) -> str:
    """Generate a random alphanumeric string"""
    import string
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))