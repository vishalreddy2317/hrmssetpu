"""
Appointment Model
Patient appointment scheduling and management
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional

from .base import BaseModel


class Appointment(BaseModel):
    """
    Appointment model for scheduling patient visits
    """
    
    __tablename__ = "appointments"
    
    # Appointment Details
    appointment_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    appointment_date: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    appointment_time: Mapped[str] = mapped_column(String(10), nullable=False)
    
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
    
    # Department
    department_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("departments.id", ondelete="SET NULL"),
        index=True
    )
    
    # Appointment Type
    appointment_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        comment="consultation, follow_up, emergency, routine_checkup, diagnostic, vaccination"
    )
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='scheduled',
        nullable=False,
        index=True,
        comment="scheduled, confirmed, in_progress, completed, cancelled, no_show, rescheduled"
    )
    
    # Duration
    duration_minutes: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    
    # Reason
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    symptoms: Mapped[Optional[str]] = mapped_column(Text)
    
    # Notes
    doctor_notes: Mapped[Optional[str]] = mapped_column(Text)
    prescription_given: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Cancellation
    cancelled_by: Mapped[Optional[str]] = mapped_column(String(50))
    cancellation_reason: Mapped[Optional[str]] = mapped_column(Text)
    cancelled_at: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Rescheduling
    rescheduled_from: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("appointments.id", ondelete="SET NULL")
    )
    rescheduled_to: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Follow-up
    is_follow_up: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    parent_appointment_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("appointments.id", ondelete="SET NULL")
    )
    next_follow_up_date: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Payment
    consultation_fee: Mapped[Optional[float]] = mapped_column(Integer)
    payment_status: Mapped[str] = mapped_column(
        String(20),
        default='pending',
        comment="pending, paid, waived"
    )
    
    # Timestamps
    checked_in_at: Mapped[Optional[str]] = mapped_column(String(50))
    checked_out_at: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Relationships
    patient: Mapped["Patient"] = relationship(
        "Patient",
        back_populates="appointments"
    )
    
    doctor: Mapped["Doctor"] = relationship(
        "Doctor",
        back_populates="appointments"
    )
    
    department: Mapped[Optional["Department"]] = relationship(
        "Department",
        back_populates="appointments"
    )
    
    parent_appointment: Mapped[Optional["Appointment"]] = relationship(
        "Appointment",
        remote_side="Appointment.id",
        foreign_keys=[parent_appointment_id],
        backref="follow_up_appointments"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name='appointment_positive_duration'),
        CheckConstraint('consultation_fee >= 0 OR consultation_fee IS NULL', name='appointment_positive_fee'),
        Index('idx_appointment_date_time', 'appointment_date', 'appointment_time'),
        Index('idx_appointment_patient', 'patient_id', 'status'),
        Index('idx_appointment_doctor', 'doctor_id', 'appointment_date'),
        Index('idx_appointment_status_date', 'status', 'appointment_date'),
        {'comment': 'Patient appointment scheduling and tracking'}
    )
    
    # Validators
    @validates('appointment_type')
    def validate_appointment_type(self, key, value):
        valid_types = [
            'consultation', 'follow_up', 'emergency', 'routine_checkup',
            'diagnostic', 'vaccination', 'therapy', 'counseling'
        ]
        if value.lower() not in valid_types:
            raise ValueError(f"Appointment type must be one of: {', '.join(valid_types)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = [
            'scheduled', 'confirmed', 'in_progress', 'completed',
            'cancelled', 'no_show', 'rescheduled'
        ]
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    @validates('payment_status')
    def validate_payment_status(self, key, value):
        valid_statuses = ['pending', 'paid', 'waived', 'refunded']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Payment status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<Appointment(id={self.id}, number='{self.appointment_number}', date='{self.appointment_date}', status='{self.status}')>"
    