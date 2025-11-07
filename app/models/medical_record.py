"""
Medical Record Model
Patient medical records and history
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional

from .base import BaseModel


class MedicalRecord(BaseModel):
    """
    Medical record model for patient health records
    """
    
    __tablename__ = "medical_records"
    
    # Record Details
    record_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    
    # Patient Reference
    patient_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Doctor Reference
    doctor_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("doctors.id", ondelete="SET NULL"),
        index=True
    )
    
    # Visit/Appointment Reference
    appointment_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("appointments.id", ondelete="SET NULL"),
        index=True
    )
    
    # Diagnosis Reference
    diagnosis_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("diagnoses.id", ondelete="SET NULL"),
        index=True
    )
    
    # Record Type
    record_type: Mapped[str] = mapped_column(
        String(50),
        default='general',
        nullable=False,
        index=True,
        comment="general, consultation, emergency, follow_up, discharge"
    )
    
    # Visit Details
    visit_date: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    visit_time: Mapped[Optional[str]] = mapped_column(String(10))
    
    # Chief Complaint
    chief_complaint: Mapped[Optional[str]] = mapped_column(Text)
    
    # Vital Signs
    temperature: Mapped[Optional[str]] = mapped_column(String(10), comment="in Fahrenheit")
    blood_pressure: Mapped[Optional[str]] = mapped_column(String(20), comment="systolic/diastolic")
    pulse_rate: Mapped[Optional[str]] = mapped_column(String(10), comment="beats per minute")
    respiratory_rate: Mapped[Optional[str]] = mapped_column(String(10))
    oxygen_saturation: Mapped[Optional[str]] = mapped_column(String(10), comment="SpO2 percentage")
    weight: Mapped[Optional[str]] = mapped_column(String(10), comment="in kg")
    height: Mapped[Optional[str]] = mapped_column(String(10), comment="in cm")
    bmi: Mapped[Optional[str]] = mapped_column(String(10))
    
    # Clinical Notes
    history_of_present_illness: Mapped[Optional[str]] = mapped_column(Text)
    past_medical_history: Mapped[Optional[str]] = mapped_column(Text)
    family_history: Mapped[Optional[str]] = mapped_column(Text)
    social_history: Mapped[Optional[str]] = mapped_column(Text)
    
    # Physical Examination
    physical_examination: Mapped[Optional[str]] = mapped_column(Text)
    
    # Assessment and Plan
    assessment: Mapped[Optional[str]] = mapped_column(Text)
    diagnosis_notes: Mapped[Optional[str]] = mapped_column(Text)
    treatment_plan: Mapped[Optional[str]] = mapped_column(Text)
    
    # Medications
    medications_prescribed: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array")
    
    # Tests Ordered
    lab_tests_ordered: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array")
    imaging_ordered: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array")
    
    # Procedures
    procedures_performed: Mapped[Optional[str]] = mapped_column(Text)
    
    # Follow-up
    follow_up_required: Mapped[bool] = mapped_column(Boolean, default=False)
    follow_up_date: Mapped[Optional[str]] = mapped_column(String(20))
    follow_up_instructions: Mapped[Optional[str]] = mapped_column(Text)
    
    # Discharge Information
    discharge_summary: Mapped[Optional[str]] = mapped_column(Text)
    discharge_date: Mapped[Optional[str]] = mapped_column(String(20))
    discharge_instructions: Mapped[Optional[str]] = mapped_column(Text)
    
    # Allergies and Alerts
    allergies: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array")
    alerts: Mapped[Optional[str]] = mapped_column(Text)
    
    # Documents
    attachments: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array of file URLs")
    
    # General Notes
    notes: Mapped[Optional[str]] = mapped_column(Text)
    doctor_notes: Mapped[Optional[str]] = mapped_column(Text)
    nurse_notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='active',
        nullable=False,
        index=True,
        comment="active, archived, amended"
    )
    
    # Confidentiality
    is_confidential: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Relationships
    patient: Mapped["Patient"] = relationship(
        "Patient",
        back_populates="medical_records"
    )
    
    doctor: Mapped[Optional["Doctor"]] = relationship(
        "Doctor",
        backref="medical_records"
    )
    
    diagnosis: Mapped[Optional["Diagnosis"]] = relationship(
        "Diagnosis",
        backref="medical_records"
    )
    
    appointment: Mapped[Optional["Appointment"]] = relationship(
        "Appointment",
        backref="medical_records"
    )
    
    # Table Arguments
    __table_args__ = (
        Index('idx_medicalrecord_patient', 'patient_id', 'visit_date'),
        Index('idx_medicalrecord_doctor', 'doctor_id', 'visit_date'),
        Index('idx_medicalrecord_type', 'record_type', 'status'),
        {'comment': 'Patient medical records and health history'}
    )
    
    # Validators
    @validates('record_type')
    def validate_record_type(self, key, value):
        valid_types = ['general', 'consultation', 'emergency', 'follow_up', 'discharge', 'admission']
        if value.lower() not in valid_types:
            raise ValueError(f"Record type must be one of: {', '.join(valid_types)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['active', 'archived', 'amended', 'deleted']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<MedicalRecord(id={self.id}, number='{self.record_number}', patient_id={self.patient_id})>"