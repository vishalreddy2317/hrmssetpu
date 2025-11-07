"""
Doctor Model
Medical staff information and specializations
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional, List
from decimal import Decimal
import re

from .base import BaseModel


class Doctor(BaseModel):
    """
    Doctor model for medical staff management
    """
    
    __tablename__ = "doctors"
    
    # User Reference
    user_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        index=True
    )
    
    # Basic Information
    doctor_id: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    middle_name: Mapped[Optional[str]] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    
    # Professional Information
    specialization: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    qualification: Mapped[str] = mapped_column(String(200), nullable=False)
    medical_license_number: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    license_expiry_date: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Experience
    years_of_experience: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    previous_hospitals: Mapped[Optional[str]] = mapped_column(Text)
    
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
    
    # Professional Details
    designation: Mapped[Optional[str]] = mapped_column(String(100))
    employee_id: Mapped[Optional[str]] = mapped_column(String(50), unique=True, index=True)
    joining_date: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Consultation
    consultation_fee: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    average_consultation_time: Mapped[int] = mapped_column(Integer, default=30, comment="minutes")
    
    # Availability
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    is_on_duty: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    max_appointments_per_day: Mapped[int] = mapped_column(Integer, default=20, nullable=False)
    
    # Ratings
    rating: Mapped[Optional[Decimal]] = mapped_column(Numeric(3, 2))
    total_ratings: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
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
    bio: Mapped[Optional[str]] = mapped_column(Text)
    languages_spoken: Mapped[Optional[str]] = mapped_column(String(200))
    awards_achievements: Mapped[Optional[str]] = mapped_column(Text)
    research_publications: Mapped[Optional[str]] = mapped_column(Text)
    profile_image: Mapped[Optional[str]] = mapped_column(String(500))
    signature_image: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Relationships
    hospital: Mapped[Optional["Hospital"]] = relationship(
        "Hospital",
        back_populates="doctors"
    )
    
    department: Mapped[Optional["Department"]] = relationship(
        "Department",
        back_populates="doctors",
        foreign_keys=[department_id]
    )
    
    departments_managed: Mapped[List["Department"]] = relationship(
        "Department",
        back_populates="head_doctor",
        foreign_keys="Department.head_doctor_id",
        lazy="dynamic"
    )
    
    patients: Mapped[List["Patient"]] = relationship(
        "Patient",
        back_populates="primary_doctor",
        lazy="dynamic"
    )
    
    appointments: Mapped[List["Appointment"]] = relationship(
        "Appointment",
        back_populates="doctor",
        lazy="dynamic"
    )
    
    prescriptions: Mapped[List["Prescription"]] = relationship(
        "Prescription",
        back_populates="doctor",
        lazy="dynamic"
    )
    
    schedules: Mapped[List["Schedule"]] = relationship(
        "Schedule",
        back_populates="doctor",
        lazy="dynamic"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('years_of_experience >= 0', name='doctor_positive_experience'),
        CheckConstraint('consultation_fee >= 0 OR consultation_fee IS NULL', name='doctor_positive_fee'),
        CheckConstraint('rating >= 0 AND rating <= 5 OR rating IS NULL', name='doctor_valid_rating'),
        CheckConstraint('average_consultation_time > 0', name='doctor_positive_consultation_time'),
        CheckConstraint('max_appointments_per_day > 0', name='doctor_positive_max_appointments'),
        Index('idx_doctor_name', 'first_name', 'last_name'),
        Index('idx_doctor_specialization', 'specialization', 'status'),
        Index('idx_doctor_hospital', 'hospital_id', 'status'),
        Index('idx_doctor_department', 'department_id', 'status'),
        Index('idx_doctor_availability', 'is_available', 'is_on_duty'),
        {'comment': 'Medical staff information and credentials'}
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
    
    # Properties
    @property
    def full_name(self) -> str:
        """Get full name with title"""
        name = f"Dr. {self.first_name}"
        if self.middle_name:
            name += f" {self.middle_name}"
        name += f" {self.last_name}"
        return name
    
    @property
    def average_rating(self) -> float:
        """Get average rating"""
        if self.rating:
            return float(self.rating)
        return 0.0
    
    def __repr__(self) -> str:
        return f"<Doctor(id={self.id}, doctor_id='{self.doctor_id}', name='{self.full_name}', specialization='{self.specialization}')>"
