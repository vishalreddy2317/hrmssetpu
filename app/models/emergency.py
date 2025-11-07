"""
Emergency Model
Emergency department cases and tracking
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional

from .base import BaseModel


class Emergency(BaseModel):
    """
    Emergency case model
    """
    
    __tablename__ = "emergencies"
    
    # Emergency Details
    emergency_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    arrival_date: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    arrival_time: Mapped[str] = mapped_column(String(10), nullable=False)
    arrival_mode: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="ambulance, walk_in, police, transferred"
    )
    
    # Patient
    patient_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Attending Doctor
    attending_doctor_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("doctors.id", ondelete="SET NULL"),
        index=True
    )
    
    # Triage
    triage_category: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
        comment="critical, urgent, semi_urgent, non_urgent, deceased"
    )
    triage_color: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="red, orange, yellow, green, blue, black"
    )
    triage_time: Mapped[Optional[str]] = mapped_column(String(10))
    triaged_by: Mapped[Optional[str]] = mapped_column(String(200))
    
    # Chief Complaint
    chief_complaint: Mapped[str] = mapped_column(Text, nullable=False)
    symptoms: Mapped[Optional[str]] = mapped_column(Text)
    
    # Vital Signs
    temperature: Mapped[Optional[str]] = mapped_column(String(10))
    blood_pressure: Mapped[Optional[str]] = mapped_column(String(20))
    pulse_rate: Mapped[Optional[str]] = mapped_column(String(10))
    respiratory_rate: Mapped[Optional[str]] = mapped_column(String(10))
    oxygen_saturation: Mapped[Optional[str]] = mapped_column(String(10))
    glasgow_coma_scale: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Medical History (at time of arrival)
    known_allergies: Mapped[Optional[str]] = mapped_column(Text)
    current_medications: Mapped[Optional[str]] = mapped_column(Text)
    medical_history: Mapped[Optional[str]] = mapped_column(Text)
    
    # Treatment
    initial_treatment: Mapped[Optional[str]] = mapped_column(Text)
    investigations_ordered: Mapped[Optional[str]] = mapped_column(Text)
    diagnosis: Mapped[Optional[str]] = mapped_column(Text)
    
    # Outcome
    disposition: Mapped[str] = mapped_column(
        String(50),
        default='under_observation',
        nullable=False,
        index=True,
        comment="admitted, discharged, transferred, deceased, left_against_advice, absconded"
    )
    disposition_time: Mapped[Optional[str]] = mapped_column(String(10))
    
    # If Admitted
    admitted_to_ward_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("wards.id", ondelete="SET NULL")
    )
    admission_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("admissions.id", ondelete="SET NULL")
    )
    
    # If Transferred
    transferred_to: Mapped[Optional[str]] = mapped_column(String(200))
    transfer_reason: Mapped[Optional[str]] = mapped_column(Text)
    
    # Ambulance (if arrived by ambulance)
    ambulance_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("ambulances.id", ondelete="SET NULL")
    )
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='in_progress',
        nullable=False,
        index=True,
        comment="in_progress, completed, cancelled"
    )
    
    # Police Case
    is_police_case: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    police_station: Mapped[Optional[str]] = mapped_column(String(200))
    fir_number: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Medico-Legal Case
    is_mlc: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    mlc_number: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Time Tracking
    door_to_doctor_time: Mapped[Optional[int]] = mapped_column(Integer, comment="minutes")
    total_time_in_er: Mapped[Optional[int]] = mapped_column(Integer, comment="minutes")
    
    # Notes
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationships
    patient: Mapped["Patient"] = relationship(
        "Patient",
        backref="emergency_visits"
    )
    
    attending_doctor: Mapped[Optional["Doctor"]] = relationship(
        "Doctor",
        backref="emergency_cases"
    )
    
    ward: Mapped[Optional["Ward"]] = relationship(
        "Ward",
        backref="emergency_admissions"
    )
    
    admission: Mapped[Optional["Admission"]] = relationship(
        "Admission",
        backref="emergency_record"
    )
    
    ambulance: Mapped[Optional["Ambulance"]] = relationship(
        "Ambulance",
        backref="emergency_cases"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('glasgow_coma_scale >= 3 AND glasgow_coma_scale <= 15 OR glasgow_coma_scale IS NULL', name='emergency_valid_gcs'),
        Index('idx_emergency_patient', 'patient_id', 'arrival_date'),
        Index('idx_emergency_triage', 'triage_category', 'status'),
        Index('idx_emergency_disposition', 'disposition', 'status'),
        {'comment': 'Emergency department cases and patient tracking'}
    )
    
    # Validators
    @validates('triage_category')
    def validate_triage_category(self, key, value):
        valid_categories = ['critical', 'urgent', 'semi_urgent', 'non_urgent', 'deceased']
        if value.lower() not in valid_categories:
            raise ValueError(f"Triage category must be one of: {', '.join(valid_categories)}")
        return value.lower()
    
    @validates('disposition')
    def validate_disposition(self, key, value):
        valid_dispositions = [
            'admitted', 'discharged', 'transferred', 'deceased',
            'left_against_advice', 'absconded', 'under_observation'
        ]
        if value.lower() not in valid_dispositions:
            raise ValueError(f"Disposition must be one of: {', '.join(valid_dispositions)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['in_progress', 'completed', 'cancelled']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<Emergency(id={self.id}, number='{self.emergency_number}', triage='{self.triage_category}')>"