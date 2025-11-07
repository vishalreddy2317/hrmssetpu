from app.models.user import User
from app.utils.auth import verify_password, generate_otp
from app.utils.two_fa_store import create_two_fa_session
from app.repositories.user import user_repository  # your existing user repo

# Step 1: verify password & generate 2FA token
async def login_user(email: str = None, phone_number: str = None, password: str = None):
    user = None
    if email:
        user = await user_repository.get_by_email(email)
    elif phone_number:
        user = await user_repository.get_by_phone(phone_number)
    
    if not user or not verify_password(password, user.password):
        return None, "Invalid credentials"
    
    otp = generate_otp()
    two_fa_token = create_two_fa_session(user.id, otp)
    
    # Send OTP to email or phone (implement your mail/SMS here)
    print(f"OTP for user {user.id}: {otp}")  # For testing
    
    return two_fa_token, None
