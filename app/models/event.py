"""
Diagnosis Model
Patient diagnosis tracking and medical coding
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional
from decimal import Decimal

from .base import BaseModel


class Diagnosis(BaseModel):
    """
    Patient diagnosis model with ICD coding and clinical details
    """
    
    __tablename__ = "diagnoses"
    
    # Basic Information
    diagnosis_code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    diagnosis_name: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Patient and Doctor References
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
    
    # Medical Coding
    icd_version: Mapped[str] = mapped_column(
        String(10),
        default='ICD-10',
        nullable=False,
        comment="ICD-9, ICD-10, ICD-11"
    )
    
    icd_code: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
        comment="ICD diagnosis code"
    )
    
    snomed_code: Mapped[Optional[str]] = mapped_column(String(50), comment="SNOMED CT code")
    
    # Classification
    diagnosis_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        comment="primary, secondary, differential, provisional, confirmed"
    )
    
    category: Mapped[Optional[str]] = mapped_column(String(100), index=True)
    
    # Severity
    severity: Mapped[str] = mapped_column(
        String(20),
        default='moderate',
        nullable=False,
        comment="mild, moderate, severe, critical"
    )
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='active',
        nullable=False,
        index=True,
        comment="active, resolved, chronic, under_observation"
    )
    
    # Dates
    diagnosis_date: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    onset_date: Mapped[Optional[str]] = mapped_column(String(20), comment="Symptom onset date")
    resolution_date: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Clinical Details
    symptoms: Mapped[Optional[str]] = mapped_column(Text, comment="Presenting symptoms")
    clinical_findings: Mapped[Optional[str]] = mapped_column(Text)
    
    # Body Location
    body_site: Mapped[Optional[str]] = mapped_column(String(200))
    laterality: Mapped[Optional[str]] = mapped_column(String(20), comment="left, right, bilateral")
    
    # Confirmation
    is_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    confirmed_by: Mapped[Optional[str]] = mapped_column(String(200))
    confirmed_date: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Treatment
    treatment_plan: Mapped[Optional[str]] = mapped_column(Text)
    medications: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array")
    
    # Prognosis
    prognosis: Mapped[Optional[str]] = mapped_column(String(50), comment="excellent, good, fair, poor")
    
    # Follow-up
    requires_followup: Mapped[bool] = mapped_column(Boolean, default=False)
    followup_date: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Chronic Management
    is_chronic: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Priority
    priority: Mapped[str] = mapped_column(String(20), default='normal', comment="low, normal, high, urgent")
    
    # Notes
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationships
    patient: Mapped["Patient"] = relationship(
        "Patient",
        back_populates="diagnoses"
    )
    
    doctor: Mapped["Doctor"] = relationship(
        "Doctor",
        back_populates="diagnoses"
    )
    
    # Table Arguments
    __table_args__ = (
        Index('idx_diagnosis_patient_date', 'patient_id', 'diagnosis_date'),
        Index('idx_diagnosis_doctor', 'doctor_id', 'diagnosis_date'),
        Index('idx_diagnosis_icd', 'icd_code', 'icd_version'),
        Index('idx_diagnosis_type_status', 'diagnosis_type', 'status'),
        {'comment': 'Patient diagnosis tracking and medical coding'}
    )
    
    # Validators
    @validates('diagnosis_type')
    def validate_diagnosis_type(self, key, value):
        valid_types = ['primary', 'secondary', 'differential', 'provisional', 'confirmed', 'rule_out']
        if value.lower() not in valid_types:
            raise ValueError(f"Diagnosis type must be one of: {', '.join(valid_types)}")
        return value.lower()
    
    @validates('severity')
    def validate_severity(self, key, value):
        valid_severities = ['mild', 'moderate', 'severe', 'critical']
        if value.lower() not in valid_severities:
            raise ValueError(f"Severity must be one of: {', '.join(valid_severities)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['active', 'resolved', 'chronic', 'under_observation', 'ruled_out']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<Diagnosis(id={self.id}, code='{self.icd_code}', patient_id={self.patient_id})>"