"""
Diagnosis Model
Patient diagnosis tracking and medical coding
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional

from .base import BaseModel


class Diagnosis(BaseModel):
    """
    Patient diagnosis model with ICD coding
    """
    
    __tablename__ = "diagnoses"
    
    # Diagnosis Details
    diagnosis_code: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    diagnosis_name: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Patient Reference
    patient_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Doctor Reference
    doctor_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("doctors.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Admission/Visit Reference (optional)
    admission_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("admissions.id", ondelete="SET NULL"),
        index=True
    )
    
    appointment_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("appointments.id", ondelete="SET NULL"),
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
    
    # Additional Coding
    snomed_code: Mapped[Optional[str]] = mapped_column(String(50), comment="SNOMED CT code")
    dms_code: Mapped[Optional[str]] = mapped_column(String(50), comment="Disease management code")
    
    # Classification
    diagnosis_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        comment="primary, secondary, differential, provisional, confirmed, rule_out"
    )
    
    category: Mapped[Optional[str]] = mapped_column(
        String(100),
        index=True,
        comment="Disease category (infectious, chronic, acute, etc.)"
    )
    
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
        comment="active, resolved, chronic, under_observation, ruled_out"
    )
    
    # Dates
    diagnosis_date: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    diagnosis_time: Mapped[Optional[str]] = mapped_column(String(10))
    onset_date: Mapped[Optional[str]] = mapped_column(String(20), comment="When symptoms started")
    resolution_date: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Clinical Details
    symptoms: Mapped[Optional[str]] = mapped_column(Text, comment="Presenting symptoms")
    clinical_findings: Mapped[Optional[str]] = mapped_column(Text, comment="Clinical examination findings")
    differential_diagnoses: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array of alternative diagnoses")
    
    # Laterality & Location
    body_site: Mapped[Optional[str]] = mapped_column(String(200), comment="Anatomical location")
    laterality: Mapped[Optional[str]] = mapped_column(
        String(20),
        comment="left, right, bilateral, unilateral"
    )
    
    # Stage/Grade (for cancers, etc.)
    stage: Mapped[Optional[str]] = mapped_column(String(50), comment="Disease stage (I, II, III, IV, etc.)")
    grade: Mapped[Optional[str]] = mapped_column(String(50), comment="Tumor grade, severity grade")
    
    # Confirmation
    is_confirmed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    confirmed_by: Mapped[Optional[str]] = mapped_column(String(200))
    confirmed_date: Mapped[Optional[str]] = mapped_column(String(20))
    confirmation_method: Mapped[Optional[str]] = mapped_column(
        String(100),
        comment="clinical, laboratory, imaging, biopsy, genetic_test"
    )
    
    # Supporting Evidence
    lab_results: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array of lab test IDs")
    imaging_results: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array of imaging IDs")
    biopsy_results: Mapped[Optional[str]] = mapped_column(Text)
    
    # Treatment
    treatment_plan: Mapped[Optional[str]] = mapped_column(Text)
    medications: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array of medications")
    procedures: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array of procedures")
    
    # Prognosis
    prognosis: Mapped[Optional[str]] = mapped_column(
        String(50),
        comment="excellent, good, fair, poor, grave"
    )
    expected_outcome: Mapped[Optional[str]] = mapped_column(Text)
    
    # Follow-up
    requires_followup: Mapped[bool] = mapped_column(Boolean, default=False)
    followup_date: Mapped[Optional[str]] = mapped_column(String(20))
    followup_frequency: Mapped[Optional[str]] = mapped_column(String(50), comment="weekly, monthly, quarterly")
    
    # Complications
    complications: Mapped[Optional[str]] = mapped_column(Text, comment="Any complications")
    comorbidities: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array of related conditions")
    
    # Risk Factors
    risk_factors: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array of risk factors")
    
    # Chronic Disease Management
    is_chronic: Mapped[bool] = mapped_column(Boolean, default=False)
    management_plan: Mapped[Optional[str]] = mapped_column(Text)
    
    # Notification/Reporting
    is_notifiable: Mapped[bool] = mapped_column(Boolean, default=False, comment="Reportable disease")
    notified_to: Mapped[Optional[str]] = mapped_column(String(200), comment="Public health authority")
    notification_date: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Priority
    priority: Mapped[str] = mapped_column(
        String(20),
        default='normal',
        comment="low, normal, high, urgent"
    )
    
    # Cost/Billing
    diagnosis_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    
    # Notes
    notes: Mapped[Optional[str]] = mapped_column(Text)
    internal_notes: Mapped[Optional[str]] = mapped_column(Text, comment="Staff-only notes")
    
    # Verification
    verified_by: Mapped[Optional[str]] = mapped_column(String(200))
    verified_date: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Relationships
    patient: Mapped["Patient"] = relationship(
        "Patient",
        back_populates="diagnoses"
    )
    
    doctor: Mapped["Doctor"] = relationship(
        "Doctor",
        back_populates="diagnoses"
    )
    
    admission: Mapped[Optional["Admission"]] = relationship(
        "Admission",
        backref="diagnoses"
    )
    
    appointment: Mapped[Optional["Appointment"]] = relationship(
        "Appointment",
        backref="diagnoses"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('diagnosis_cost >= 0 OR diagnosis_cost IS NULL', name='diagnosis_positive_cost'),
        Index('idx_diagnosis_patient', 'patient_id', 'diagnosis_date'),
        Index('idx_diagnosis_doctor', 'doctor_id', 'diagnosis_date'),
        Index('idx_diagnosis_icd', 'icd_code', 'icd_version'),
        Index('idx_diagnosis_type_status', 'diagnosis_type', 'status'),
        Index('idx_diagnosis_category', 'category', 'status'),
        {'comment': 'Patient diagnosis tracking and medical coding'}
    )
    
    # Validators
    @validates('diagnosis_type')
    def validate_diagnosis_type(self, key, value):
        valid_types = [
            'primary', 'secondary', 'differential', 'provisional',
            'confirmed', 'rule_out', 'working', 'admission', 'discharge'
        ]
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
        valid_statuses = [
            'active', 'resolved', 'chronic', 'under_observation',
            'ruled_out', 'inactive', 'recurrent'
        ]
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    @validates('icd_version')
    def validate_icd_version(self, key, value):
        valid_versions = ['ICD-9', 'ICD-10', 'ICD-11']
        if value.upper() not in valid_versions:
            raise ValueError(f"ICD version must be one of: {', '.join(valid_versions)}")
        return value.upper()
    
    def __repr__(self) -> str:
        return f"<Diagnosis(id={self.id}, code='{self.icd_code}', name='{self.diagnosis_name}', patient_id={self.patient_id})>"