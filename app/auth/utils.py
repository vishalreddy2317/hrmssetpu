"""
✅ Auth utilities - SINGLE SOURCE OF TRUTH
Handles JWT, password hashing, and OTP
"""
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import secrets
import string
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.models import OTPCode
from app.core.config import settings

# ============================================================
# Password Hashing
# ============================================================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plaintext password"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against hash"""
    return pwd_context.verify(plain_password, hashed_password)


# ============================================================
# JWT Token Functions
# ============================================================

def create_jwt_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT token with expiry"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    secret = settings.get_jwt_secret()
    return jwt.encode(to_encode, secret, algorithm=settings.JWT_ALGORITHM)


def create_access_token(user_id: int) -> str:
    """Generate an access token"""
    return create_jwt_token(
        {"sub": str(user_id), "type": "access"},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )


def create_refresh_token(user_id: int) -> str:
    """Generate a refresh token"""
    return create_jwt_token(
        {"sub": str(user_id), "type": "refresh"},
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )


def verify_token(token: str):
    """Verify and decode a JWT token"""
    try:
        secret = settings.get_jwt_secret()
        return jwt.decode(token, secret, algorithms=[settings.JWT_ALGORITHM])
    except JWTError as e:
        print(f"[JWT ERROR] {e}")
        return None


# ============================================================
# OTP Functions
# ============================================================

def generate_otp_code(length: int = None) -> str:
    """Generate a numeric OTP code"""
    length = length or settings.OTP_LENGTH
    return ''.join(secrets.choice(string.digits) for _ in range(length))


async def create_otp_code(db: AsyncSession, user_id: int, purpose: str, method: str) -> str:
    """
    Create a new OTP, deleting any previous unused OTPs.
    Returns the generated code.
    """
    try:
        # Delete previous unused OTPs for same user/purpose
        await db.execute(
            delete(OTPCode).where(
                OTPCode.user_id == user_id,
                OTPCode.purpose == purpose,
                OTPCode.is_used == False
            )
        )

        # Generate new OTP
        code = generate_otp_code()
        expires_at = datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)

        new_otp = OTPCode(
            user_id=user_id,
            code=code,
            purpose=purpose,
            method=method,
            expires_at=expires_at
        )

        db.add(new_otp)
        await db.commit()
        await db.refresh(new_otp)

        print(f"[DEBUG] OTP created for user_id={user_id}, purpose={purpose}: {code}")
        return code
        
    except Exception as e:
        await db.rollback()
        print(f"[ERROR] Failed to create OTP: {e}")
        raise


async def verify_otp_code(db: AsyncSession, user_id: int, otp_code: str, purpose: str) -> bool:
    """
    Verify an OTP and mark it as used.
    Returns True if verified successfully.
    """
    try:
        result = await db.execute(
            select(OTPCode).where(
                OTPCode.user_id == user_id,
                OTPCode.code == otp_code,
                OTPCode.purpose == purpose,
                OTPCode.is_used == False
            )
        )
        otp_record = result.scalars().first()

        if not otp_record:
            print(f"[DEBUG] OTP not found for user_id={user_id}")
            return False

        if otp_record.is_expired():
            print(f"[DEBUG] OTP expired for user_id={user_id}")
            return False

        # Mark as used
        otp_record.is_used = True
        await db.commit()
        print(f"[DEBUG] OTP verified for user_id={user_id}")
        return True

    except Exception as e:
        await db.rollback()
        print(f"[ERROR] OTP verification failed: {e}")
        return False