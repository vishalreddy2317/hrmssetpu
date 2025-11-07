"""
✅ Auth Models - PRIMARY source of truth for User
This is used for authentication AND user management
"""
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base


class User(Base):
    """
    ✅ MAIN User model - used everywhere in the app
    Single source of truth for users table
    """
    __tablename__ = "users"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Authentication fields
    email = Column(String(120), unique=True, index=True, nullable=True)
    phone = Column(String(20), unique=True, index=True, nullable=True)
    username = Column(String(100), unique=True, index=True, nullable=True)
    password_hash = Column(String(255), nullable=False)
    
    # Profile fields
    full_name = Column(String(200), nullable=True)
    
    # Authorization
    role = Column(String(50), nullable=False, default='user')  # user, admin, doctor, nurse, patient, staff
    
    # Status flags
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Additional info
    address = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    otp_codes = relationship(
        "OTPCode",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class OTPCode(Base):
    """
    ✅ OTP tracking for 2FA authentication
    """
    __tablename__ = "otp_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    code = Column(String(6), nullable=False)
    purpose = Column(String(50), nullable=False)  # 'login', 'verify_email', 'verify_phone'
    method = Column(String(10), nullable=False)   # 'email', 'sms'
    expires_at = Column(DateTime, nullable=False)
    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="otp_codes")
    
    def is_expired(self):
        """Check if OTP has expired"""
        return datetime.utcnow() > self.expires_at