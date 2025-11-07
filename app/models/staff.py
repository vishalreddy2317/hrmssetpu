"""
Staff Model
Administrative and support staff management
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional, List
from decimal import Decimal
import re

from .base import BaseModel


class Staff(BaseModel):
    """
    Staff model for administrative and support personnel
    """
    
    __tablename__ = "staffs"
    
    # User Reference
    user_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        index=True
    )
    
    # Basic Information
    staff_id: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    middle_name: Mapped[Optional[str]] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    
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
    
    # Employment Details
    employee_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    designation: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    department: Mapped[Optional[str]] = mapped_column(String(100), index=True)
    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        comment="receptionist, accountant, hr, admin, security, housekeeping, lab_technician, pharmacist"
    )
    
    # Hospital Assignment
    hospital_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("hospitals.id", ondelete="SET NULL"),
        index=True
    )
    
    # Work Details
    joining_date: Mapped[str] = mapped_column(String(20), nullable=False)
    leaving_date: Mapped[Optional[str]] = mapped_column(String(20))
    shift: Mapped[Optional[str]] = mapped_column(
        String(20),
        comment="morning, evening, night, rotating, general"
    )
    
    # Salary
    salary: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2))
    salary_currency: Mapped[str] = mapped_column(String(3), default="USD")
    
    # Qualifications
    qualification: Mapped[str] = mapped_column(String(200), nullable=False)
    experience_years: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Availability
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_on_duty: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='active',
        nullable=False,
        index=True,
        comment="active, on_leave, resigned, terminated, retired"
    )
    
    # Emergency Contact
    emergency_contact_name: Mapped[Optional[str]] = mapped_column(String(200))
    emergency_contact_phone: Mapped[Optional[str]] = mapped_column(String(20))
    emergency_contact_relation: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Identification
    national_id: Mapped[Optional[str]] = mapped_column(String(50), unique=True)
    
    # Additional Information
    skills: Mapped[Optional[str]] = mapped_column(Text)
    certifications: Mapped[Optional[str]] = mapped_column(Text)
    languages_spoken: Mapped[Optional[str]] = mapped_column(String(200))
    notes: Mapped[Optional[str]] = mapped_column(Text)
    profile_image: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Relationships
    hospital: Mapped[Optional["Hospital"]] = relationship(
        "Hospital",
        backref="staff_members"
    )
    
    attendances: Mapped[List["Attendance"]] = relationship(
        "Attendance",
        back_populates="staff",
        lazy="dynamic"
    )
    
    leaves: Mapped[List["Leave"]] = relationship(
        "Leave",
        back_populates="staff",
        lazy="dynamic"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('experience_years >= 0', name='staff_positive_experience'),
        CheckConstraint('salary > 0 OR salary IS NULL', name='staff_positive_salary'),
        Index('idx_staff_name', 'first_name', 'last_name'),
        Index('idx_staff_role', 'role', 'status'),
        Index('idx_staff_hospital', 'hospital_id', 'status'),
        {'comment': 'Administrative and support staff management'}
    )
    
    # Validators
    @validates('email')
    def validate_email(self, key, value):
        if value and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise ValueError("Invalid email format")
        return value
    
    @validates('role')
    def validate_role(self, key, value):
        valid_roles = [
            'receptionist', 'accountant', 'hr', 'admin', 'security',
            'housekeeping', 'lab_technician', 'pharmacist', 'it_support',
            'maintenance', 'dietitian', 'social_worker'
        ]
        if value.lower() not in valid_roles:
            raise ValueError(f"Role must be one of: {', '.join(valid_roles)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['active', 'on_leave', 'resigned', 'terminated', 'retired', 'suspended']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    @property
    def full_name(self) -> str:
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self) -> str:
        return f"<Staff(id={self.id}, staff_id='{self.staff_id}', name='{self.full_name}', role='{self.role}')>"
    
