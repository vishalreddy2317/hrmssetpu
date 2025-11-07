"""
Patient Model
Core patient information and medical records
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, Date, ForeignKey, Index, CheckConstraint, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional, List
from decimal import Decimal
import re

from .base import BaseModel


class Patient(BaseModel):
    """
    Patient model for managing patient information
    """
    
    __tablename__ = "patients"
    
    # Basic Information
    patient_id: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    middle_name: Mapped[Optional[str]] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    
    # Demographics
    date_of_birth: Mapped[str] = mapped_column(String(20), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
        comment="male, female, other"
    )
    
    # Contact Information
    email: Mapped[Optional[str]] = mapped_column(String(100), index=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    alternate_phone: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Address
    address: Mapped[str] = mapped_column(Text, nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), default="USA")
    pincode: Mapped[str] = mapped_column(String(20), nullable=False)
    
    # Emergency Contact
    emergency_contact_name: Mapped[str] = mapped_column(String(200), nullable=False)
    emergency_contact_phone: Mapped[str] = mapped_column(String(20), nullable=False)
    emergency_contact_relation: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Medical Information
    blood_group: Mapped[Optional[str]] = mapped_column(
        String(5),
        index=True,
        comment="A+, A-, B+, B-, AB+, AB-, O+, O-"
    )
    height_cm: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2))
    weight_kg: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2))
    bmi: Mapped[Optional[Decimal]] = mapped_column(Numeric(4, 2))
    
    # Medical History
    allergies: Mapped[Optional[str]] = mapped_column(Text)
    chronic_diseases: Mapped[Optional[str]] = mapped_column(Text)
    current_medications: Mapped[Optional[str]] = mapped_column(Text)
    medical_history: Mapped[Optional[str]] = mapped_column(Text)
    family_medical_history: Mapped[Optional[str]] = mapped_column(Text)
    
    # Hospital Assignment
    hospital_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("hospitals.id", ondelete="SET NULL"),
        index=True
    )
    primary_doctor_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("doctors.id", ondelete="SET NULL"),
        index=True
    )
    
    # Current Status
    current_bed_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("beds.id", ondelete="SET NULL")
    )
    is_admitted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    admission_date: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Insurance
    has_insurance: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    insurance_provider: Mapped[Optional[str]] = mapped_column(String(200))
    insurance_policy_number: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Identification
    national_id: Mapped[Optional[str]] = mapped_column(String(50), unique=True, index=True)
    passport_number: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='active',
        nullable=False,
        index=True,
        comment="active, discharged, deceased, transferred"
    )
    
    # Additional Info
    occupation: Mapped[Optional[str]] = mapped_column(String(100))
    marital_status: Mapped[Optional[str]] = mapped_column(String(20))
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationships
    hospital: Mapped[Optional["Hospital"]] = relationship(
        "Hospital",
        back_populates="patients"
    )
    
    primary_doctor: Mapped[Optional["Doctor"]] = relationship(
        "Doctor",
        back_populates="patients",
        foreign_keys=[primary_doctor_id]
    )
    
    current_bed: Mapped[Optional["Bed"]] = relationship(
        "Bed",
        back_populates="current_patient",
        foreign_keys=[current_bed_id]
    )
    
    appointments: Mapped[List["Appointment"]] = relationship(
        "Appointment",
        back_populates="patient",
        lazy="dynamic"
    )
    
    admissions: Mapped[List["Admission"]] = relationship(
        "Admission",
        back_populates="patient",
        lazy="dynamic"
    )
    
    prescriptions: Mapped[List["Prescription"]] = relationship(
        "Prescription",
        back_populates="patient",
        lazy="dynamic"
    )
    
    lab_tests: Mapped[List["LabTest"]] = relationship(
        "LabTest",
        back_populates="patient",
        lazy="dynamic"
    )
    
    billings: Mapped[List["Billing"]] = relationship(
        "Billing",
        back_populates="patient",
        lazy="dynamic"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('age >= 0 AND age <= 150', name='patient_valid_age'),
        CheckConstraint('height_cm > 0 OR height_cm IS NULL', name='patient_positive_height'),
        CheckConstraint('weight_kg > 0 OR weight_kg IS NULL', name='patient_positive_weight'),
        Index('idx_patient_name', 'first_name', 'last_name'),
        Index('idx_patient_hospital', 'hospital_id', 'status'),
        Index('idx_patient_doctor', 'primary_doctor_id'),
        Index('idx_patient_admitted', 'is_admitted', 'status'),
        {'comment': 'Patient information and medical records'}
    )
    
    # Validators
    @validates('email')
    def validate_email(self, key, value):
        """Validate email format"""
        if value and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise ValueError("Invalid email format")
        return value
    
    @validates('gender')
    def validate_gender(self, key, value):
        """Validate gender"""
        valid_genders = ['male', 'female', 'other']
        if value.lower() not in valid_genders:
            raise ValueError(f"Gender must be one of: {', '.join(valid_genders)}")
        return value.lower()
    
    @validates('blood_group')
    def validate_blood_group(self, key, value):
        """Validate blood group"""
        if value:
            valid_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
            if value.upper() not in valid_groups:
                raise ValueError(f"Blood group must be one of: {', '.join(valid_groups)}")
            return value.upper()
        return value
    
    @validates('status')
    def validate_status(self, key, value):
        """Validate status"""
        valid_statuses = ['active', 'discharged', 'deceased', 'transferred', 'inactive']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    # Properties
    @property
    def full_name(self) -> str:
        """Get full name"""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_address(self) -> str:
        """Get complete address"""
        return f"{self.address}, {self.city}, {self.state} {self.pincode}, {self.country}"
    
    def calculate_bmi(self) -> Optional[Decimal]:
        """Calculate BMI from height and weight"""
        if self.height_cm and self.weight_kg:
            height_m = self.height_cm / 100
            bmi = self.weight_kg / (height_m ** 2)
            self.bmi = round(bmi, 2)
            return self.bmi
        return None
    
    def __repr__(self) -> str:
        return f"<Patient(id={self.id}, patient_id='{self.patient_id}', name='{self.full_name}')>"