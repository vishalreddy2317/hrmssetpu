"""
Nurse Model
Nursing staff information and assignments
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional, List
import re

from .base import BaseModel


class Nurse(BaseModel):
    """
    Nurse model for nursing staff management
    """
    
    __tablename__ = "nurses"
    
    # User Reference
    user_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        index=True
    )
    
    # Basic Information
    nurse_id: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    middle_name: Mapped[Optional[str]] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    
    # Professional Information
    qualification: Mapped[str] = mapped_column(String(200), nullable=False)
    nursing_license_number: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    license_expiry_date: Mapped[Optional[str]] = mapped_column(String(20))
    specialization: Mapped[Optional[str]] = mapped_column(String(100), index=True)
    
    # Experience
    years_of_experience: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Contact Information
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    alternate_phone: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Address
    address: Mapped[str] = mapped_column(Text, nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), default="USA")
    pincode: Mapped[str] = mapped_column(String(20), nullable=False)
    
    # Hospital Assignment
    hospital_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("hospitals.id", ondelete="SET NULL"),
        index=True
    )
    department_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("departments.id", ondelete="SET NULL"),
        index=True
    )
    
    # Work Details
    designation: Mapped[Optional[str]] = mapped_column(String(100))
    employee_id: Mapped[Optional[str]] = mapped_column(String(50), unique=True, index=True)
    joining_date: Mapped[Optional[str]] = mapped_column(String(20))
    shift: Mapped[Optional[str]] = mapped_column(
        String(20),
        comment="morning, evening, night, rotating"
    )
    
    # Availability
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    is_on_duty: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='active',
        nullable=False,
        index=True,
        comment="active, on_leave, resigned, retired, suspended"
    )
    
    # Emergency Contact
    emergency_contact_name: Mapped[Optional[str]] = mapped_column(String(200))
    emergency_contact_phone: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Additional Information
    certifications: Mapped[Optional[str]] = mapped_column(Text)
    languages_spoken: Mapped[Optional[str]] = mapped_column(String(200))
    profile_image: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Relationships
    hospital: Mapped[Optional["Hospital"]] = relationship(
        "Hospital",
        back_populates="nurses"
    )
    
    department: Mapped[Optional["Department"]] = relationship(
        "Department",
        back_populates="nurses"
    )
    
    wards_managed: Mapped[List["Ward"]] = relationship(
        "Ward",
        back_populates="head_nurse",
        foreign_keys="Ward.head_nurse_id",
        lazy="dynamic"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('years_of_experience >= 0', name='nurse_positive_experience'),
        Index('idx_nurse_name', 'first_name', 'last_name'),
        Index('idx_nurse_hospital', 'hospital_id', 'status'),
        Index('idx_nurse_department', 'department_id', 'status'),
        Index('idx_nurse_availability', 'is_available', 'is_on_duty'),
        {'comment': 'Nursing staff information and assignments'}
    )
    
    # Validators
    @validates('email')
    def validate_email(self, key, value):
        """Validate email format"""
        if value and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise ValueError("Invalid email format")
        return value
    
    @validates('status')
    def validate_status(self, key, value):
        """Validate status"""
        valid_statuses = ['active', 'on_leave', 'resigned', 'retired', 'suspended', 'inactive']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    @validates('shift')
    def validate_shift(self, key, value):
        """Validate shift"""
        if value:
            valid_shifts = ['morning', 'evening', 'night', 'rotating']
            if value.lower() not in valid_shifts:
                raise ValueError(f"Shift must be one of: {', '.join(valid_shifts)}")
            return value.lower()
        return value
    
    # Properties
    @property
    def full_name(self) -> str:
        """Get full name"""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self) -> str:
        return f"<Nurse(id={self.id}, nurse_id='{self.nurse_id}', name='{self.full_name}')>"