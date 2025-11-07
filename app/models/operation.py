"""
Operation Model
Surgical procedures and operation theater management
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional
from decimal import Decimal

from .base import BaseModel


class Operation(BaseModel):
    """
    Surgical operation/procedure model
    """
    
    __tablename__ = "operations"
    
    # Operation Details
    operation_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    
    # Patient
    patient_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Admission
    admission_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("admissions.id", ondelete="SET NULL"),
        index=True
    )
    
    # Surgery Details
    surgery_name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    surgery_code: Mapped[Optional[str]] = mapped_column(String(50))
    surgery_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="elective, emergency, minor, major"
    )
    
    # Pre-operative Diagnosis
    pre_operative_diagnosis: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Post-operative Diagnosis
    post_operative_diagnosis: Mapped[Optional[str]] = mapped_column(Text)
    
    # Surgeons
    primary_surgeon_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("doctors.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    assistant_surgeons: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array")
    
    # Anesthesia
    anesthesiologist_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("doctors.id", ondelete="SET NULL")
    )
    anesthesia_type: Mapped[Optional[str]] = mapped_column(
        String(50),
        comment="general, spinal, epidural, local, sedation"
    )
    
    # Scheduling
    scheduled_date: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    scheduled_start_time: Mapped[str] = mapped_column(String(10), nullable=False)
    scheduled_end_time: Mapped[str] = mapped_column(String(10), nullable=False)
    
    # Actual Timing
    actual_start_time: Mapped[Optional[str]] = mapped_column(String(10))
    actual_end_time: Mapped[Optional[str]] = mapped_column(String(10))
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Operation Theater
    ot_number: Mapped[Optional[str]] = mapped_column(String(20))
    ot_floor: Mapped[Optional[int]] = mapped_column(Integer)  # ⭐ Floor reference
    
    # Procedure Details
    procedure_description: Mapped[Optional[str]] = mapped_column(Text)
    findings: Mapped[Optional[str]] = mapped_column(Text)
    complications: Mapped[Optional[str]] = mapped_column(Text)
    
    # Implants/Prosthetics
    implants_used: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array")
    
    # Blood
    blood_loss_ml: Mapped[Optional[int]] = mapped_column(Integer)
    blood_transfusion: Mapped[bool] = mapped_column(Boolean, default=False)
    blood_units_transfused: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='scheduled',
        nullable=False,
        index=True,
        comment="scheduled, in_progress, completed, cancelled, postponed"
    )
    
    # Priority
    priority: Mapped[str] = mapped_column(
        String(20),
        default='routine',
        nullable=False,
        comment="emergency, urgent, routine"
    )
    
    # Outcome
    outcome: Mapped[Optional[str]] = mapped_column(
        String(50),
        comment="successful, complicated, unsuccessful"
    )
    
    # Post-operative Care
    icu_required: Mapped[bool] = mapped_column(Boolean, default=False)
    ventilator_required: Mapped[bool] = mapped_column(Boolean, default=False)
    recovery_room: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Instructions
    post_op_instructions: Mapped[Optional[str]] = mapped_column(Text)
    discharge_instructions: Mapped[Optional[str]] = mapped_column(Text)
    
    # Cost
    estimated_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2))
    actual_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2))
    
    # Consent
    consent_obtained: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    consent_document_url: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Notes
    notes: Mapped[Optional[str]] = mapped_column(Text)
    operation_notes_url: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Relationships
    patient: Mapped["Patient"] = relationship(
        "Patient",
        backref="operations"
    )
    
    admission: Mapped[Optional["Admission"]] = relationship(
        "Admission",
        backref="operations"
    )
    
    primary_surgeon: Mapped["Doctor"] = relationship(
        "Doctor",
        foreign_keys=[primary_surgeon_id],
        backref="surgeries_performed"
    )
    
    anesthesiologist: Mapped[Optional["Doctor"]] = relationship(
        "Doctor",
        foreign_keys=[anesthesiologist_id],
        backref="anesthesia_provided"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('duration_minutes >= 0 OR duration_minutes IS NULL', name='operation_positive_duration'),
        CheckConstraint('blood_loss_ml >= 0 OR blood_loss_ml IS NULL', name='operation_positive_blood_loss'),
        CheckConstraint('blood_units_transfused >= 0 OR blood_units_transfused IS NULL', name='operation_positive_blood_units'),
        CheckConstraint('estimated_cost >= 0 OR estimated_cost IS NULL', name='operation_positive_estimated_cost'),
        CheckConstraint('actual_cost >= 0 OR actual_cost IS NULL', name='operation_positive_actual_cost'),
        Index('idx_operation_patient', 'patient_id', 'scheduled_date'),
        Index('idx_operation_surgeon', 'primary_surgeon_id', 'scheduled_date'),
        Index('idx_operation_date_status', 'scheduled_date', 'status'),
        {'comment': 'Surgical operations and procedures'}
    )
    
    # Validators
    @validates('surgery_type')
    def validate_surgery_type(self, key, value):
        valid_types = ['elective', 'emergency', 'minor', 'major', 'day_care']
        if value.lower() not in valid_types:
            raise ValueError(f"Surgery type must be one of: {', '.join(valid_types)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['scheduled', 'in_progress', 'completed', 'cancelled', 'postponed']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    @validates('priority')
    def validate_priority(self, key, value):
        valid_priorities = ['emergency', 'urgent', 'routine']
        if value.lower() not in valid_priorities:
            raise ValueError(f"Priority must be one of: {', '.join(valid_priorities)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<Operation(id={self.id}, number='{self.operation_number}', surgery='{self.surgery_name}', status='{self.status}')>"