from fastapi import APIRouter, HTTPException
from app.schemas.auth import LoginRequest, OTPRequest, TokenResponse
from app.services.auth_service import login_user
from app.utils.auth import create_access_token
from app.utils.two_fa_store import verify_two_fa

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
async def login(request: LoginRequest):
    two_fa_token, error = await login_user(
        email=request.email, phone_number=request.phone_number, password=request.password
    )
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"two_fa_token": two_fa_token, "message": "OTP sent to your email/phone"}

@router.post("/verify-otp", response_model=TokenResponse)
async def verify_otp(request: OTPRequest):
    valid, user_id = verify_two_fa(request.two_fa_token, request.otp)
    if not valid:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    access_token = create_access_token({"sub": str(user_id)})
    return {"access_token": access_token, "expires_in": 3600}
