"""
Procedure Model
Medical procedures performed on patients
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional
from decimal import Decimal

from .base import BaseModel


class Procedure(BaseModel):
    """
    Medical procedure model
    """
    
    __tablename__ = "procedures"
    
    # Procedure Details
    procedure_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    
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
    
    # Procedure Information
    procedure_name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    procedure_code: Mapped[Optional[str]] = mapped_column(String(50), index=True)
    
    # Category
    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        comment="surgical, diagnostic, therapeutic, preventive"
    )
    
    # Type
    procedure_type: Mapped[str] = mapped_column(
        String(50),
        default='minor',
        nullable=False,
        comment="minor, major, emergency, elective"
    )
    
    # Description
    description: Mapped[Optional[str]] = mapped_column(Text)
    indications: Mapped[Optional[str]] = mapped_column(Text)
    
    # Scheduling
    scheduled_date: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    scheduled_time: Mapped[str] = mapped_column(String(10), nullable=False)
    procedure_date: Mapped[Optional[str]] = mapped_column(String(20), index=True)
    procedure_time: Mapped[Optional[str]] = mapped_column(String(10))
    
    # Duration
    estimated_duration: Mapped[Optional[int]] = mapped_column(Integer, comment="Duration in minutes")
    actual_duration: Mapped[Optional[int]] = mapped_column(Integer, comment="Actual duration in minutes")
    
    # Location
    room_number: Mapped[Optional[str]] = mapped_column(String(50))
    operation_theater: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Staff Involved
    assisting_doctors: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array")
    nurses_assigned: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array")
    anesthetist: Mapped[Optional[str]] = mapped_column(String(200))
    
    # Anesthesia
    anesthesia_type: Mapped[Optional[str]] = mapped_column(
        String(50),
        comment="local, general, regional, sedation, none"
    )
    anesthesia_notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Pre-Procedure
    pre_procedure_instructions: Mapped[Optional[str]] = mapped_column(Text)
    pre_procedure_tests: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array")
    consent_obtained: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    consent_date: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Procedure Details
    findings: Mapped[Optional[str]] = mapped_column(Text)
    technique_used: Mapped[Optional[str]] = mapped_column(Text)
    complications: Mapped[Optional[str]] = mapped_column(Text)
    
    # Specimens
    specimens_collected: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array")
    pathology_required: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Post-Procedure
    post_procedure_instructions: Mapped[Optional[str]] = mapped_column(Text)
    recovery_notes: Mapped[Optional[str]] = mapped_column(Text)
    discharge_time: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Follow-up
    follow_up_required: Mapped[bool] = mapped_column(Boolean, default=False)
    follow_up_date: Mapped[Optional[str]] = mapped_column(String(20))
    follow_up_instructions: Mapped[Optional[str]] = mapped_column(Text)
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='scheduled',
        nullable=False,
        index=True,
        comment="scheduled, in_progress, completed, cancelled, postponed"
    )
    
    # Outcome
    outcome: Mapped[Optional[str]] = mapped_column(
        String(50),
        comment="successful, unsuccessful, partial_success"
    )
    
    # Priority
    priority: Mapped[str] = mapped_column(
        String(20),
        default='routine',
        nullable=False,
        comment="routine, urgent, emergency"
    )
    
    # Cost
    estimated_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    actual_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    
    # Documents
    procedure_report_url: Mapped[Optional[str]] = mapped_column(String(500))
    images_urls: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array")
    consent_form_url: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Notes
    doctor_notes: Mapped[Optional[str]] = mapped_column(Text)
    nurse_notes: Mapped[Optional[str]] = mapped_column(Text)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationships
    patient: Mapped["Patient"] = relationship(
        "Patient",
        back_populates="procedures"
    )
    
    doctor: Mapped["Doctor"] = relationship(
        "Doctor",
        back_populates="procedures"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('estimated_duration > 0 OR estimated_duration IS NULL', name='procedure_positive_est_duration'),
        CheckConstraint('actual_duration > 0 OR actual_duration IS NULL', name='procedure_positive_act_duration'),
        CheckConstraint('estimated_cost >= 0 OR estimated_cost IS NULL', name='procedure_positive_est_cost'),
        CheckConstraint('actual_cost >= 0 OR actual_cost IS NULL', name='procedure_positive_act_cost'),
        Index('idx_procedure_patient', 'patient_id', 'scheduled_date'),
        Index('idx_procedure_doctor', 'doctor_id', 'scheduled_date'),
        Index('idx_procedure_status', 'status', 'priority'),
        Index('idx_procedure_date', 'procedure_date', 'status'),
        {'comment': 'Medical procedures performed on patients'}
    )
    
    # Validators
    @validates('category')
    def validate_category(self, key, value):
        valid_categories = ['surgical', 'diagnostic', 'therapeutic', 'preventive', 'cosmetic']
        if value.lower() not in valid_categories:
            raise ValueError(f"Category must be one of: {', '.join(valid_categories)}")
        return value.lower()
    
    @validates('procedure_type')
    def validate_procedure_type(self, key, value):
        valid_types = ['minor', 'major', 'emergency', 'elective']
        if value.lower() not in valid_types:
            raise ValueError(f"Procedure type must be one of: {', '.join(valid_types)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['scheduled', 'in_progress', 'completed', 'cancelled', 'postponed']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    @validates('priority')
    def validate_priority(self, key, value):
        valid_priorities = ['routine', 'urgent', 'emergency']
        if value.lower() not in valid_priorities:
            raise ValueError(f"Priority must be one of: {', '.join(valid_priorities)}")
        return value.lower()
    
    @validates('anesthesia_type')
    def validate_anesthesia_type(self, key, value):
        if value:
            valid_types = ['local', 'general', 'regional', 'sedation', 'none']
            if value.lower() not in valid_types:
                raise ValueError(f"Anesthesia type must be one of: {', '.join(valid_types)}")
            return value.lower()
        return value
    
    def __repr__(self) -> str:
        return f"<Procedure(id={self.id}, number='{self.procedure_number}', name='{self.procedure_name}')>"