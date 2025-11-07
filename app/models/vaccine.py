"""
Vaccine Model
Vaccination and immunization records
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional

from .base import BaseModel


class Vaccine(BaseModel):
    """
    Vaccination record model
    """
    
    __tablename__ = "vaccines"
    
    # Vaccination Record Details
    vaccination_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    
    # Patient and Doctor
    patient_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    doctor_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("doctors.id", ondelete="SET NULL"),
        index=True
    )
    
    # Vaccine Details
    vaccine_name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    vaccine_code: Mapped[Optional[str]] = mapped_column(String(50))
    
    vaccine_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        comment="covid_19, influenza, hepatitis_a, hepatitis_b, mmr, polio, tetanus, etc."
    )
    
    # Manufacturer Details
    manufacturer: Mapped[str] = mapped_column(String(200), nullable=False)
    batch_number: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    lot_number: Mapped[Optional[str]] = mapped_column(String(100))
    
    expiry_date: Mapped[str] = mapped_column(String(20), nullable=False)
    
    # Dose Information
    dose_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    total_doses_required: Mapped[Optional[int]] = mapped_column(Integer)
    dosage: Mapped[Optional[str]] = mapped_column(String(50), comment="0.5ml, 1ml, etc.")
    
    # Administration Details
    administered_date: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    administered_time: Mapped[str] = mapped_column(String(10), nullable=False)
    
    administered_by: Mapped[str] = mapped_column(String(200), nullable=False)
    nurse_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("nurses.id", ondelete="SET NULL")
    )
    
    # Site of Injection
    site_of_injection: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="left_arm, right_arm, left_thigh, right_thigh, etc."
    )
    route_of_administration: Mapped[str] = mapped_column(
        String(50),
        default='intramuscular',
        comment="intramuscular, subcutaneous, oral, intranasal"
    )
    
    # Next Dose
    next_dose_due: Mapped[bool] = mapped_column(Boolean, default=False)
    next_dose_date: Mapped[Optional[str]] = mapped_column(String(20), index=True)
    next_dose_number: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Pre-Vaccination Screening
    temperature: Mapped[Optional[str]] = mapped_column(String(10))
    blood_pressure: Mapped[Optional[str]] = mapped_column(String(20))
    
    screening_done: Mapped[bool] = mapped_column(Boolean, default=True)
    contraindications_checked: Mapped[bool] = mapped_column(Boolean, default=True)
    consent_obtained: Mapped[bool] = mapped_column(Boolean, default=True)
    consent_form_url: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Adverse Reactions
    has_adverse_reaction: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    adverse_reactions: Mapped[Optional[str]] = mapped_column(Text)
    reaction_severity: Mapped[Optional[str]] = mapped_column(
        String(20),
        comment="mild, moderate, severe"
    )
    reaction_reported: Mapped[bool] = mapped_column(Boolean, default=False)
    reaction_report_number: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Post-Vaccination Observation
    observation_period_minutes: Mapped[int] = mapped_column(Integer, default=15)
    observation_notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Vaccination Certificate
    certificate_number: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
    certificate_url: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Storage Conditions Verification
    storage_temperature_verified: Mapped[bool] = mapped_column(Boolean, default=True)
    cold_chain_maintained: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Campaign/Program
    vaccination_program: Mapped[Optional[str]] = mapped_column(String(200))
    is_part_of_campaign: Mapped[bool] = mapped_column(Boolean, default=False)
    campaign_name: Mapped[Optional[str]] = mapped_column(String(200))
    
    # Cost
    is_free: Mapped[bool] = mapped_column(Boolean, default=False)
    cost: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Notes
    notes: Mapped[Optional[str]] = mapped_column(Text)
    doctor_notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='completed',
        nullable=False,
        comment="scheduled, completed, cancelled, postponed"
    )
    
    # Relationships
    patient: Mapped["Patient"] = relationship(
        "Patient",
        back_populates="vaccinations"
    )
    
    doctor: Mapped[Optional["Doctor"]] = relationship(
        "Doctor",
        backref="vaccinations_prescribed"
    )
    
    nurse: Mapped[Optional["Nurse"]] = relationship(
        "Nurse",
        backref="vaccinations_administered"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('dose_number > 0', name='vaccine_positive_dose_number'),
        CheckConstraint('observation_period_minutes >= 0', name='vaccine_positive_observation'),
        Index('idx_vaccine_patient', 'patient_id', 'administered_date'),
        Index('idx_vaccine_type', 'vaccine_type', 'dose_number'),
        Index('idx_vaccine_batch', 'batch_number', 'expiry_date'),
        Index('idx_vaccine_next_dose', 'next_dose_date', 'patient_id'),
        {'comment': 'Vaccination and immunization records'}
    )
    
    # Validators
    @validates('vaccine_type')
    def validate_vaccine_type(cls, v):
        valid = [
            'covid_19', 'influenza', 'hepatitis_a', 'hepatitis_b', 'mmr',
            'polio', 'tetanus', 'dpt', 'bcg', 'hpv', 'meningitis',
            'pneumonia', 'rabies', 'typhoid', 'yellow_fever', 'cholera'
        ]
        if v.lower() not in valid:
            raise ValueError(f"Vaccine type must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validates('route_of_administration')
    def validate_route(cls, v):
        valid = ['intramuscular', 'subcutaneous', 'oral', 'intranasal', 'intradermal']
        if v.lower() not in valid:
            raise ValueError(f"Route must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validates('status')
    def validate_status(cls, v):
        valid = ['scheduled', 'completed', 'cancelled', 'postponed', 'missed']
        if v.lower() not in valid:
            raise ValueError(f"Status must be one of: {', '.join(valid)}")
        return v.lower()
    
    def __repr__(self) -> str:
        return f"<Vaccine(id={self.id}, name='{self.vaccine_name}', dose={self.dose_number})>"