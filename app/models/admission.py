"""
Admission Model
Patient admission tracking and management
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional
from decimal import Decimal

from .base import BaseModel


class Admission(BaseModel):
    """
    Patient admission model
    """
    
    __tablename__ = "admissions"
    
    # Admission Details
    admission_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    admission_date: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    admission_time: Mapped[str] = mapped_column(String(10), nullable=False)
    
    # Patient
    patient_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Doctor
    admitting_doctor_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("doctors.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Location
    room_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("rooms.id", ondelete="SET NULL"),
        index=True
    )
    bed_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("beds.id", ondelete="SET NULL"),
        index=True
    )
    ward_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("wards.id", ondelete="SET NULL"),
        index=True
    )
    
    # Admission Type
    admission_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        comment="emergency, planned, transfer, observation"
    )
    
    # Reason
    diagnosis: Mapped[str] = mapped_column(Text, nullable=False)
    symptoms: Mapped[Optional[str]] = mapped_column(Text)
    chief_complaint: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='admitted',
        nullable=False,
        index=True,
        comment="admitted, discharged, transferred, deceased"
    )
    
    # Discharge Information
    discharge_date: Mapped[Optional[str]] = mapped_column(String(20))
    discharge_time: Mapped[Optional[str]] = mapped_column(String(10))
    discharge_type: Mapped[Optional[str]] = mapped_column(
        String(50),
        comment="normal, against_medical_advice, transferred, deceased"
    )
    
    # Medical Details
    vital_signs: Mapped[Optional[str]] = mapped_column(Text, comment="JSON format")
    allergies: Mapped[Optional[str]] = mapped_column(Text)
    current_medications: Mapped[Optional[str]] = mapped_column(Text)
    
    # Treatment
    treatment_plan: Mapped[Optional[str]] = mapped_column(Text)
    special_instructions: Mapped[Optional[str]] = mapped_column(Text)
    
    # Insurance
    insurance_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("insurances.id", ondelete="SET NULL")
    )
    insurance_approved: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Financial
    estimated_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2))
    advance_payment: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2))
    
    # Notes
    admission_notes: Mapped[Optional[str]] = mapped_column(Text)
    discharge_summary: Mapped[Optional[str]] = mapped_column(Text)
    
    # Duration
    expected_duration_days: Mapped[Optional[int]] = mapped_column(Integer)
    actual_duration_days: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Relationships
    patient: Mapped["Patient"] = relationship(
        "Patient",
        back_populates="admissions"
    )
    
    admitting_doctor: Mapped["Doctor"] = relationship(
        "Doctor",
        backref="admissions"
    )
    
    room: Mapped[Optional["Room"]] = relationship(
        "Room",
        back_populates="admissions"
    )
    
    bed: Mapped[Optional["Bed"]] = relationship(
        "Bed",
        back_populates="admissions"
    )
    
    ward: Mapped[Optional["Ward"]] = relationship(
        "Ward",
        back_populates="admissions"
    )
    
    insurance: Mapped[Optional["Insurance"]] = relationship(
        "Insurance",
        backref="admissions"
    )
    
    discharge_record: Mapped[Optional["Discharge"]] = relationship(
        "Discharge",
        back_populates="admission",
        uselist=False
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('estimated_cost >= 0 OR estimated_cost IS NULL', name='admission_positive_estimated_cost'),
        CheckConstraint('advance_payment >= 0 OR advance_payment IS NULL', name='admission_positive_advance_payment'),
        CheckConstraint('expected_duration_days > 0 OR expected_duration_days IS NULL', name='admission_positive_expected_duration'),
        Index('idx_admission_patient', 'patient_id', 'status'),
        Index('idx_admission_doctor', 'admitting_doctor_id'),
        Index('idx_admission_date', 'admission_date', 'status'),
        Index('idx_admission_room_bed', 'room_id', 'bed_id'),
        {'comment': 'Patient admission records and tracking'}
    )
    
    # Validators
    @validates('admission_type')
    def validate_admission_type(self, key, value):
        valid_types = ['emergency', 'planned', 'transfer', 'observation', 'day_care']
        if value.lower() not in valid_types:
            raise ValueError(f"Admission type must be one of: {', '.join(valid_types)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['admitted', 'discharged', 'transferred', 'deceased', 'under_observation']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<Admission(id={self.id}, number='{self.admission_number}', patient_id={self.patient_id}, status='{self.status}')>"
    