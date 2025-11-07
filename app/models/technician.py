"""
Technician Model
Lab and Radiology technicians management
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional, List
from decimal import Decimal
import re

from .base import BaseModel


class Technician(BaseModel):
    """
    Technician model for lab and radiology staff
    """
    
    __tablename__ = "technicians"
    
    # User Reference
    user_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        index=True
    )
    
    # Basic Information
    employee_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    middle_name: Mapped[Optional[str]] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    
    # Professional Details
    specialization: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        comment="lab, radiology, ecg, eeg, dialysis, physiotherapy, pathology"
    )
    qualification: Mapped[str] = mapped_column(String(200), nullable=False)
    license_number: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
    license_expiry_date: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Experience
    years_of_experience: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Contact Information
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    alternate_phone: Mapped[Optional[str]] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    
    # Address
    address: Mapped[str] = mapped_column(Text, nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), default="USA")
    pincode: Mapped[str] = mapped_column(String(20), nullable=False)
    
    # Employment Details
    department: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        comment="laboratory, radiology, cardiology, etc."
    )
    department_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("departments.id", ondelete="SET NULL"),
        index=True
    )
    
    designation: Mapped[Optional[str]] = mapped_column(String(100))
    joining_date: Mapped[str] = mapped_column(String(20), nullable=False)
    leaving_date: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Work Schedule
    shift: Mapped[Optional[str]] = mapped_column(
        String(20),
        comment="morning, evening, night, rotating"
    )
    
    # Salary
    salary: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2))
    salary_currency: Mapped[str] = mapped_column(String(3), default="USD")
    
    # Availability
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    is_on_duty: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='active',
        nullable=False,
        index=True,
        comment="active, on_leave, resigned, terminated, retired"
    )
    
    # Skills & Certifications
    skills: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array of skills")
    certifications: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array of certifications")
    training_completed: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array")
    
    # Emergency Contact
    emergency_contact_name: Mapped[Optional[str]] = mapped_column(String(200))
    emergency_contact_phone: Mapped[Optional[str]] = mapped_column(String(20))
    emergency_contact_relation: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Additional Info
    languages_spoken: Mapped[Optional[str]] = mapped_column(String(200))
    notes: Mapped[Optional[str]] = mapped_column(Text)
    profile_image: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Identification
    national_id: Mapped[Optional[str]] = mapped_column(String(50), unique=True)
    
    # Relationships
    user: Mapped[Optional["User"]] = relationship(
        "User",
        backref="technician_profile"
    )
    
    department_rel: Mapped[Optional["Department"]] = relationship(
        "Department",
        backref="technicians"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('years_of_experience >= 0', name='technician_positive_experience'),
        CheckConstraint('salary > 0 OR salary IS NULL', name='technician_positive_salary'),
        Index('idx_technician_name', 'first_name', 'last_name'),
        Index('idx_technician_specialization', 'specialization', 'status'),
        Index('idx_technician_department', 'department', 'status'),
        {'comment': 'Lab and radiology technicians management'}
    )
    
    # Validators
    @validates('email')
    def validate_email(self, key, value):
        if value and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise ValueError("Invalid email format")
        return value
    
    @validates('specialization')
    def validate_specialization(self, key, value):
        valid = [
            'lab', 'radiology', 'ecg', 'eeg', 'dialysis',
            'physiotherapy', 'pathology', 'blood_bank', 'microbiology',
            'biochemistry', 'ct_scan', 'mri', 'ultrasound', 'x_ray'
        ]
        if value.lower() not in valid:
            raise ValueError(f"Specialization must be one of: {', '.join(valid)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        valid = ['active', 'on_leave', 'resigned', 'terminated', 'retired', 'suspended']
        if value.lower() not in valid:
            raise ValueError(f"Status must be one of: {', '.join(valid)}")
        return value.lower()
    
    @property
    def full_name(self) -> str:
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self) -> str:
        return f"<Technician(id={self.id}, employee_id='{self.employee_id}', name='{self.full_name}')>"