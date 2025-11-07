"""
Prescription Model
Doctor prescriptions for patients
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional, List

from .base import BaseModel
from app.core.database import Base


# Association table for prescription-medicine many-to-many relationship
prescription_medicines = Table(
    'prescription_medicines',
    Base.metadata,
    Column('prescription_id', Integer, ForeignKey('prescriptions.id', ondelete='CASCADE'), primary_key=True),
    Column('medicine_id', Integer, ForeignKey('medicines.id', ondelete='CASCADE'), primary_key=True),
    Column('dosage', String(100), nullable=False),
    Column('frequency', String(100), nullable=False),
    Column('duration', String(50), nullable=False),
    Column('quantity', Integer, nullable=False),
    Column('instructions', Text),
    Column('created_at', String(50)),
    Index('idx_prescription_medicine', 'prescription_id', 'medicine_id')
)


class Prescription(BaseModel):
    """
    Medical prescription model
    """
    
    __tablename__ = "prescriptions"
    
    # Prescription Details
    prescription_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    prescription_date: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    
    # Patient and Doctor
    patient_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    doctor_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("doctors.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Related Appointment/Admission
    appointment_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("appointments.id", ondelete="SET NULL"),
        index=True
    )
    admission_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("admissions.id", ondelete="SET NULL")
    )
    
    # Diagnosis
    diagnosis: Mapped[str] = mapped_column(Text, nullable=False)
    symptoms: Mapped[Optional[str]] = mapped_column(Text)
    
    # Prescription Type
    prescription_type: Mapped[str] = mapped_column(
        String(50),
        default='outpatient',
        nullable=False,
        comment="outpatient, inpatient, emergency, followup"
    )
    
    # Vital Signs (at time of prescription)
    temperature: Mapped[Optional[str]] = mapped_column(String(10))
    blood_pressure: Mapped[Optional[str]] = mapped_column(String(20))
    pulse_rate: Mapped[Optional[str]] = mapped_column(String(10))
    respiratory_rate: Mapped[Optional[str]] = mapped_column(String(10))
    
    # Instructions
    general_instructions: Mapped[Optional[str]] = mapped_column(Text)
    dietary_advice: Mapped[Optional[str]] = mapped_column(Text)
    precautions: Mapped[Optional[str]] = mapped_column(Text)
    
    # Follow-up
    follow_up_required: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    follow_up_date: Mapped[Optional[str]] = mapped_column(String(20))
    follow_up_notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Lab Tests Recommended
    lab_tests_recommended: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array")
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='active',
        nullable=False,
        index=True,
        comment="active, completed, cancelled, expired"
    )
    
    # Validity
    valid_until: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Digital Signature
    digital_signature: Mapped[Optional[str]] = mapped_column(String(500))
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Dispensed Status
    is_dispensed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    dispensed_by: Mapped[Optional[str]] = mapped_column(String(100))
    dispensed_at: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Notes
    doctor_notes: Mapped[Optional[str]] = mapped_column(Text)
    pharmacy_notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationships
    patient: Mapped["Patient"] = relationship(
        "Patient",
        back_populates="prescriptions"
    )
    
    doctor: Mapped["Doctor"] = relationship(
        "Doctor",
        back_populates="prescriptions"
    )
    
    appointment: Mapped[Optional["Appointment"]] = relationship(
        "Appointment",
        backref="prescriptions"
    )
    
    medicines: Mapped[List["Medicine"]] = relationship(
        "Medicine",
        secondary=prescription_medicines,
        back_populates="prescriptions",
        lazy="dynamic"
    )
    
    # Table Arguments
    __table_args__ = (
        Index('idx_prescription_patient', 'patient_id', 'prescription_date'),
        Index('idx_prescription_doctor', 'doctor_id', 'prescription_date'),
        Index('idx_prescription_status', 'status', 'is_dispensed'),
        {'comment': 'Medical prescriptions with medicine details'}
    )
    
    # Validators
    @validates('prescription_type')
    def validate_prescription_type(self, key, value):
        valid_types = ['outpatient', 'inpatient', 'emergency', 'followup', 'discharge']
        if value.lower() not in valid_types:
            raise ValueError(f"Prescription type must be one of: {', '.join(valid_types)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['active', 'completed', 'cancelled', 'expired', 'partially_dispensed']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<Prescription(id={self.id}, number='{self.prescription_number}', patient_id={self.patient_id})>"