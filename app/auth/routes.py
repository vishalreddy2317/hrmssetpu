
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select
# from app.core.database import get_db_session
# from app.auth.models import User
# from app.auth.schemas import (
#     UserRegistration, Login, VerifyOTP, Token
# )
# from app.auth.utils import (
#     hash_password, verify_password, create_access_token,
#     create_refresh_token, verify_otp_code, verify_token
# )
# from app.auth.services import send_otp

# router = APIRouter(prefix="/auth", tags=["authentication"])


# @router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
# async def register(user_data: UserRegistration, db: AsyncSession = Depends(get_db_session)):
#     # Check if user already exists (email)
#     if user_data.email:
#         result = await db.execute(select(User).filter(User.email == user_data.email))
#         if result.scalar_one_or_none():
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

#     # Check if phone number exists
#     if user_data.phone:
#         result = await db.execute(select(User).filter(User.phone == user_data.phone))
#         if result.scalar_one_or_none():
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone number already registered")

#     # Create user
#     user = User(
#         email=user_data.email,
#         phone=user_data.phone,
#         password_hash=hash_password(user_data.password),  # Fixed column name
#         role=user_data.role
#     )

#     db.add(user)
#     await db.commit()
#     await db.refresh(user)

#     # Send OTP
#     purpose = 'verify_email' if user_data.email else 'verify_phone'
#     if not await send_otp(db, user, purpose):
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to send OTP")

#     return {"message": "User registered successfully. Please verify your account with OTP.", "user_id": user.id}


# @router.post("/login", response_model=dict)
# async def login(login_data: Login, db: AsyncSession = Depends(get_db_session)):
#     # Find user
#     result = await db.execute(select(User).filter(
#         User.email == login_data.email if login_data.email else User.phone == login_data.phone
#     ))
#     user = result.scalar_one_or_none()

#     if not user or not verify_password(login_data.password, user.password_hash):  # Fixed column name
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

#     # Send OTP for login
#     if not await send_otp(db, user, 'login'):
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to send OTP")

#     return {"message": "OTP sent successfully", "method": "email" if user.email else "sms", "user_id": user.id}


# @router.post("/verify-otp", response_model=Token)
# async def verify_otp(otp_data: VerifyOTP, db: AsyncSession = Depends(get_db_session)):
#     # Find user
#     result = await db.execute(select(User).filter(
#         User.email == otp_data.email if otp_data.email else User.phone == otp_data.phone
#     ))
#     user = result.scalar_one_or_none()

#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

#     # Verify OTP
#     if not await verify_otp_code(db, user.id, otp_data.otp_code, 'login'):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired OTP")

#     # Generate tokens
#     return Token(
#         access_token=create_access_token(user.id),
#         refresh_token=create_refresh_token(user.id),
#         token_type="bearer"
#     )


# @router.post("/verify-account", response_model=dict)
# async def verify_account(otp_data: VerifyOTP, db: AsyncSession = Depends(get_db_session)):
#     # Find user
#     result = await db.execute(select(User).filter(
#         User.email == otp_data.email if otp_data.email else User.phone == otp_data.phone
#     ))
#     user = result.scalar_one_or_none()

#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

#     purpose = 'verify_email' if otp_data.email else 'verify_phone'

#     # Verify OTP
#     if not await verify_otp_code(db, user.id, otp_data.otp_code, purpose):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired OTP")

#     # Mark verified
#     user.is_verified = True
#     await db.commit()

#     return {"message": "Account verified successfully"}


# @router.post("/refresh", response_model=dict)
# async def refresh_token(refresh_token: str, db: AsyncSession = Depends(get_db_session)):
#     payload = verify_token(refresh_token)
#     if not payload or payload.get('type') != 'refresh':
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

#     user_id = int(payload.get('sub'))
#     result = await db.execute(select(User).filter(User.id == user_id))
#     user = result.scalar_one_or_none()

#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

#     return {"access_token": create_access_token(user.id), "token_type": "bearer"}


# @router.post("/resend-otp", response_model=dict)
# async def resend_otp(login_data: Login, db: AsyncSession = Depends(get_db_session)):
#     result = await db.execute(select(User).filter(
#         User.email == login_data.email if login_data.email else User.phone == login_data.phone
#     ))
#     user = result.scalar_one_or_none()

#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

#     # Resend OTP
#     if not await send_otp(db, user, 'login'):
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to send OTP")

#     return {"message": "OTP resent successfully", "method": "email" if user.email else "sms"}

# app/auth/routes.py

"""
✅ Auth routes - registration, login, OTP verification
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.auth.models import User
from app.auth.schemas import (
    UserRegistration, Login, VerifyOTP, Token, UserResponse
)
from app.auth.utils import (
    hash_password, verify_password,
    create_access_token, create_refresh_token,
    verify_otp_code, verify_token
)
from app.auth.services import send_otp

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegistration, db: AsyncSession = Depends(get_db)):
    """Register a new user"""
    
    # Check if email already exists
    if user_data.email:
        result = await db.execute(select(User).where(User.email == user_data.email))
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

    # Check if phone already exists
    if user_data.phone:
        result = await db.execute(select(User).where(User.phone == user_data.phone))
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number already registered"
            )
    
    # Check if username already exists
    if user_data.username:
        result = await db.execute(select(User).where(User.username == user_data.username))
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )

    # Create user
    user = User(
        email=user_data.email,
        phone=user_data.phone,
        username=user_data.username,
        password_hash=hash_password(user_data.password),
        full_name=user_data.full_name,
        role=user_data.role
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    # Send OTP for verification
    purpose = "verify_email" if user_data.email else "verify_phone"
    otp_sent = await send_otp(
        db, 
        user.id, 
        email=user.email, 
        phone=user.phone, 
        purpose=purpose
    )
    
    if not otp_sent:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send OTP"
        )

    return {
        "message": "User registered successfully. Please verify your account with OTP.",
        "user_id": user.id
    }


@router.post("/login", response_model=dict)
async def login(login_data: Login, db: AsyncSession = Depends(get_db)):
    """Login with email/phone and password"""
    
    # Find user
    if login_data.email:
        result = await db.execute(select(User).where(User.email == login_data.email))
    else:
        result = await db.execute(select(User).where(User.phone == login_data.phone))
    
    user = result.scalar_one_or_none()

    # Verify credentials
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Send OTP for 2FA
    otp_sent = await send_otp(
        db,
        user.id,
        email=user.email,
        phone=user.phone,
        purpose='login'
    )
    
    if not otp_sent:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send OTP"
        )

    return {
        "message": "OTP sent successfully",
        "method": "email" if user.email else "sms",
        "user_id": user.id
    }


@router.post("/verify-otp", response_model=Token)
async def verify_otp(otp_data: VerifyOTP, db: AsyncSession = Depends(get_db)):
    """Verify OTP and get access tokens"""
    
    # Find user
    if otp_data.email:
        result = await db.execute(select(User).where(User.email == otp_data.email))
    else:
        result = await db.execute(select(User).where(User.phone == otp_data.phone))
    
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Verify OTP
    otp_valid = await verify_otp_code(db, user.id, otp_data.otp_code, 'login')
    
    if not otp_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired OTP"
        )

    # Generate tokens
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/verify-account", response_model=dict)
async def verify_account(otp_data: VerifyOTP, db: AsyncSession = Depends(get_db)):
    """Verify account with OTP after registration"""
    
    # Find user
    if otp_data.email:
        result = await db.execute(select(User).where(User.email == otp_data.email))
        purpose = 'verify_email'
    else:
        result = await db.execute(select(User).where(User.phone == otp_data.phone))
        purpose = 'verify_phone'

    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Verify OTP
    otp_valid = await verify_otp_code(db, user.id, otp_data.otp_code, purpose)
    
    if not otp_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired OTP"
        )

    # Mark user as verified
    user.is_verified = True
    await db.commit()

    return {"message": "Account verified successfully"}


@router.post("/refresh", response_model=dict)
async def refresh_token_endpoint(refresh_token: str, db: AsyncSession = Depends(get_db)):
    """Get new access token using refresh token"""
    
    payload = verify_token(refresh_token)
    
    if not payload or payload.get('type') != 'refresh':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    user_id = int(payload.get('sub'))
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Generate new access token
    new_access_token = create_access_token(user.id)
    
    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }


@router.post("/resend-otp", response_model=dict)
async def resend_otp(login_data: Login, db: AsyncSession = Depends(get_db)):
    """Resend OTP to user"""
    
    # Find user
    if login_data.email:
        result = await db.execute(select(User).where(User.email == login_data.email))
    else:
        result = await db.execute(select(User).where(User.phone == login_data.phone))
    
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Resend OTP
    otp_sent = await send_otp(
        db,
        user.id,
        email=user.email,
        phone=user.phone,
        purpose='login'
    )
    
    if not otp_sent:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send OTP"
        )

    return {
        "message": "OTP resent successfully",
        "method": "email" if user.email else "sms"
    }