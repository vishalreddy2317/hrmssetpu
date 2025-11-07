"""
✅ Auth services - handles OTP sending
"""
import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
from app.auth.utils import create_otp_code
from sqlalchemy.ext.asyncio import AsyncSession


class EmailService:
    """Email service for sending OTPs"""
    
    @staticmethod
    async def send_otp_email(email: str, otp_code: str, retries: int = 1) -> bool:
        """Send OTP email asynchronously"""
        for attempt in range(1, retries + 2):
            try:
                # Check if SMTP is configured
                if not all([settings.EMAIL_SERVER, settings.EMAIL_FROM, settings.EMAIL_PASSWORD]):
                    print(f"[DEV MODE] OTP for {email}: {otp_code}")
                    return True  # Success in dev mode

                # Create email
                message = MIMEMultipart()
                message["From"] = settings.EMAIL_FROM
                message["To"] = email
                message["Subject"] = "Your OTP Code - Hospital Management"

                body = f"""
                Your OTP code is: {otp_code}
                
                This code will expire in {settings.OTP_EXPIRY_MINUTES} minutes.
                
                If you didn't request this, please ignore this email.
                
                Best regards,
                Hospital Management System
                """
                
                html_body = f"""
                <html>
                <body>
                    <h2>Hospital Management System</h2>
                    <p>Your OTP code is: <strong style="font-size: 24px;">{otp_code}</strong></p>
                    <p>This code will expire in {settings.OTP_EXPIRY_MINUTES} minutes.</p>
                    <p>If you didn't request this, please ignore this email.</p>
                </body>
                </html>
                """

                message.attach(MIMEText(body, "plain"))
                message.attach(MIMEText(html_body, "html"))

                # Send email in thread (blocking operation)
                def send_blocking():
                    with smtplib.SMTP(settings.EMAIL_SERVER, settings.EMAIL_PORT) as server:
                        server.starttls()
                        server.login(settings.EMAIL_FROM, settings.EMAIL_PASSWORD)
                        server.send_message(message)

                await asyncio.to_thread(send_blocking)
                print(f"[SUCCESS] OTP email sent to {email}")
                return True

            except Exception as e:
                print(f"[EMAIL ERROR] Attempt {attempt} failed: {e}")
                if attempt == retries + 1:
                    return False
                await asyncio.sleep(0.5)


class SMSService:
    """SMS service for sending OTPs"""
    
    @staticmethod
    async def send_otp_sms(phone: str, otp_code: str, retries: int = 1) -> bool:
        """Send OTP via SMS (mock implementation)"""
        for attempt in range(1, retries + 2):
            try:
                # TODO: Integrate with Twilio, AWS SNS, or other SMS provider
                await asyncio.sleep(0.1)  # Simulate async delay
                print(f"[DEV MODE] SMS OTP for {phone}: {otp_code}")
                return True
                
            except Exception as e:
                print(f"[SMS ERROR] Attempt {attempt} failed: {e}")
                if attempt == retries + 1:
                    return False
                await asyncio.sleep(0.5)


async def send_otp(
    db: AsyncSession, 
    user_id: int, 
    email: str = None, 
    phone: str = None, 
    purpose: str = "login"
) -> bool:
    """
    Create and send OTP to user.
    
    Args:
        db: Database session
        user_id: ID of the user
        email: User's email (if sending via email)
        phone: User's phone (if sending via SMS)
        purpose: Purpose of OTP (login, verify_email, verify_phone)
    
    Returns:
        bool: True if OTP sent successfully
    """
    method = "email" if email else "sms"
    
    # Create OTP in database
    otp_code = await create_otp_code(db, user_id, purpose, method)
    
    # Send OTP
    if method == "email" and email:
        return await EmailService.send_otp_email(email, otp_code)
    elif method == "sms" and phone:
        return await SMSService.send_otp_sms(phone, otp_code)
    else:
        print(f"[ERROR] No valid contact method provided")
        return False