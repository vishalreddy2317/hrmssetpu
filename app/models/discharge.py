"""
Discharge Model
Patient discharge records
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional

from .base import BaseModel


class Discharge(BaseModel):
    """
    Patient discharge record model
    """
    
    __tablename__ = "discharges"
    
    # Discharge Details
    discharge_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    discharge_date: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    discharge_time: Mapped[str] = mapped_column(String(10), nullable=False)
    
    # References
    admission_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("admissions.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True
    )
    patient_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    discharging_doctor_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("doctors.id", ondelete="CASCADE"),
        nullable=False
    )
    
    # Discharge Type
    discharge_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        comment="normal, against_medical_advice, transferred, deceased, absconded"
    )
    
    # Medical Summary
    final_diagnosis: Mapped[str] = mapped_column(Text, nullable=False)
    treatment_summary: Mapped[str] = mapped_column(Text, nullable=False)
    procedures_performed: Mapped[Optional[str]] = mapped_column(Text)
    complications: Mapped[Optional[str]] = mapped_column(Text)
    
    # Condition at Discharge
    condition_at_discharge: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="improved, stable, deteriorated, critical, expired"
    )
    
    # Follow-up
    follow_up_required: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    follow_up_date: Mapped[Optional[str]] = mapped_column(String(20))
    follow_up_doctor_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("doctors.id", ondelete="SET NULL")
    )
    follow_up_instructions: Mapped[Optional[str]] = mapped_column(Text)
    
    # Medications
    discharge_medications: Mapped[Optional[str]] = mapped_column(Text)
    medication_instructions: Mapped[Optional[str]] = mapped_column(Text)
    
    # Instructions
    diet_instructions: Mapped[Optional[str]] = mapped_column(Text)
    activity_restrictions: Mapped[Optional[str]] = mapped_column(Text)
    general_instructions: Mapped[Optional[str]] = mapped_column(Text)
    warning_signs: Mapped[Optional[str]] = mapped_column(Text)
    
    # Documents
    discharge_summary_url: Mapped[Optional[str]] = mapped_column(String(500))
    medical_certificate_url: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Transfer Details (if applicable)
    transferred_to_facility: Mapped[Optional[str]] = mapped_column(String(200))
    transfer_reason: Mapped[Optional[str]] = mapped_column(Text)
    
    # Death Details (if applicable)
    death_time: Mapped[Optional[str]] = mapped_column(String(10))
    cause_of_death: Mapped[Optional[str]] = mapped_column(Text)
    death_certificate_number: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Notes
    discharge_notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationships
    admission: Mapped["Admission"] = relationship(
        "Admission",
        back_populates="discharge_record"
    )
    
    patient: Mapped["Patient"] = relationship(
        "Patient",
        backref="discharge_records"
    )
    
    discharging_doctor: Mapped["Doctor"] = relationship(
        "Doctor",
        foreign_keys=[discharging_doctor_id],
        backref="discharges_performed"
    )
    
    follow_up_doctor: Mapped[Optional["Doctor"]] = relationship(
        "Doctor",
        foreign_keys=[follow_up_doctor_id],
        backref="follow_up_discharges"
    )
    
    # Table Arguments
    __table_args__ = (
        Index('idx_discharge_patient', 'patient_id', 'discharge_date'),
        Index('idx_discharge_admission', 'admission_id'),
        Index('idx_discharge_type', 'discharge_type'),
        {'comment': 'Patient discharge records and summaries'}
    )
    
    # Validators
    @validates('discharge_type')
    def validate_discharge_type(self, key, value):
        valid_types = [
            'normal', 'against_medical_advice', 'transferred',
            'deceased', 'absconded', 'referred'
        ]
        if value.lower() not in valid_types:
            raise ValueError(f"Discharge type must be one of: {', '.join(valid_types)}")
        return value.lower()
    
    @validates('condition_at_discharge')
    def validate_condition(self, key, value):
        valid_conditions = ['improved', 'stable', 'deteriorated', 'critical', 'expired', 'recovered']
        if value.lower() not in valid_conditions:
            raise ValueError(f"Condition must be one of: {', '.join(valid_conditions)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<Discharge(id={self.id}, number='{self.discharge_number}', patient_id={self.patient_id})>"