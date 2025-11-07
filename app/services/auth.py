from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user import user_repository
from app.utils.jwt import create_access_token

async def request_otp(db: AsyncSession, email: str = None, phone_number: str = None):
    user = await user_repository.get_or_create(db, email=email, phone_number=phone_number)
    otp = await user_repository.update_otp(db, user)
    # TODO: Send OTP via SMS or Email
    return {"user_id": user.id, "otp": otp}

async def verify_otp(db: AsyncSession, email: str = None, phone_number: str = None, otp_code: str = None):
    user = await user_repository.get_by_email_or_phone(db, email=email, phone_number=phone_number)
    if not user:
        return None
    valid = await user_repository.verify_otp(db, user, otp_code)
    if not valid:
        return None
    token = create_access_token({"user_id": user.id, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}
