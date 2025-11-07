"""
Radiology Model
Radiology and imaging tests and reports
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional
from decimal import Decimal

from .base import BaseModel


class Radiology(BaseModel):
    """
    Radiology and imaging test model
    """
    
    __tablename__ = "radiology"
    
    # Radiology Details
    radiology_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    
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
    
    # Imaging Type
    imaging_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        comment="x_ray, mri, ct_scan, ultrasound, pet_scan, mammography, fluoroscopy"
    )
    
    # Test Details
    test_name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    test_code: Mapped[Optional[str]] = mapped_column(String(50))
    body_part: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Category
    category: Mapped[str] = mapped_column(
        String(100),
        default='diagnostic',
        nullable=False,
        comment="diagnostic, therapeutic, interventional"
    )
    
    # Order Information
    order_date: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    order_time: Mapped[str] = mapped_column(String(10), nullable=False)
    
    # Appointment/Scheduling
    appointment_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("appointments.id", ondelete="SET NULL")
    )
    scheduled_date: Mapped[Optional[str]] = mapped_column(String(20), index=True)
    scheduled_time: Mapped[Optional[str]] = mapped_column(String(10))
    
    # Imaging Date
    date_taken: Mapped[Optional[str]] = mapped_column(String(20), index=True)
    time_taken: Mapped[Optional[str]] = mapped_column(String(10))
    
    # Clinical Information
    clinical_history: Mapped[Optional[str]] = mapped_column(Text)
    symptoms: Mapped[Optional[str]] = mapped_column(Text)
    indications: Mapped[Optional[str]] = mapped_column(Text)
    provisional_diagnosis: Mapped[Optional[str]] = mapped_column(Text)
    
    # Contrast/Preparation
    contrast_used: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    contrast_type: Mapped[Optional[str]] = mapped_column(String(100))
    contrast_volume: Mapped[Optional[str]] = mapped_column(String(50))
    
    preparation_required: Mapped[bool] = mapped_column(Boolean, default=False)
    preparation_instructions: Mapped[Optional[str]] = mapped_column(Text)
    
    # Technician/Radiologist
    technician_name: Mapped[Optional[str]] = mapped_column(String(200))
    radiologist_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("doctors.id", ondelete="SET NULL")
    )
    radiologist_name: Mapped[Optional[str]] = mapped_column(String(200))
    
    # Report
    report_status: Mapped[str] = mapped_column(
        String(20),
        default='pending',
        nullable=False,
        index=True,
        comment="pending, preliminary, final, addendum"
    )
    
    findings: Mapped[Optional[str]] = mapped_column(Text)
    impression: Mapped[Optional[str]] = mapped_column(Text)
    recommendations: Mapped[Optional[str]] = mapped_column(Text)
    
    report_date: Mapped[Optional[str]] = mapped_column(String(20), index=True)
    report_time: Mapped[Optional[str]] = mapped_column(String(10))
    
    # Result Classification
    result_type: Mapped[Optional[str]] = mapped_column(
        String(50),
        comment="normal, abnormal, critical, inconclusive"
    )
    
    # Critical Findings
    is_critical: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    critical_findings: Mapped[Optional[str]] = mapped_column(Text)
    critical_notified: Mapped[bool] = mapped_column(Boolean, default=False)
    notified_at: Mapped[Optional[str]] = mapped_column(String(50))
    notified_to: Mapped[Optional[str]] = mapped_column(String(200))
    
    # Files and Images
    report_file_url: Mapped[Optional[str]] = mapped_column(String(500))
    images_urls: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array of image URLs")
    dicom_study_id: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='ordered',
        nullable=False,
        index=True,
        comment="ordered, scheduled, in_progress, completed, cancelled, rejected"
    )
    
    # Priority
    priority: Mapped[str] = mapped_column(
        String(20),
        default='routine',
        nullable=False,
        comment="routine, urgent, stat"
    )
    
    # Quality
    image_quality: Mapped[Optional[str]] = mapped_column(String(50), comment="excellent, good, adequate, poor")
    quality_notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Equipment
    equipment_used: Mapped[Optional[str]] = mapped_column(String(200))
    machine_id: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Radiation (for applicable imaging types)
    radiation_dose: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Cost
    test_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    
    # Comparison
    comparison_studies: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array of previous study references")
    
    # Follow-up
    follow_up_required: Mapped[bool] = mapped_column(Boolean, default=False)
    follow_up_recommendations: Mapped[Optional[str]] = mapped_column(Text)
    follow_up_date: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Verification
    verified_by: Mapped[Optional[str]] = mapped_column(String(200))
    verified_at: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Notes
    technician_notes: Mapped[Optional[str]] = mapped_column(Text)
    radiologist_notes: Mapped[Optional[str]] = mapped_column(Text)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Rejection
    rejection_reason: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationships
    patient: Mapped["Patient"] = relationship(
        "Patient",
        backref="radiology_tests"
    )
    
    doctor: Mapped["Doctor"] = relationship(
        "Doctor",
        foreign_keys=[doctor_id],
        back_populates="radiology_records"
    )
    
    radiologist: Mapped[Optional["Doctor"]] = relationship(
        "Doctor",
        foreign_keys=[radiologist_id],
        backref="radiology_reports_reviewed"
    )
    
    appointment: Mapped[Optional["Appointment"]] = relationship(
        "Appointment",
        backref="radiology_tests"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('test_cost >= 0 OR test_cost IS NULL', name='radiology_positive_cost'),
        Index('idx_radiology_patient', 'patient_id', 'order_date'),
        Index('idx_radiology_doctor', 'doctor_id', 'order_date'),
        Index('idx_radiology_imaging_type', 'imaging_type', 'status'),
        Index('idx_radiology_status', 'status', 'priority'),
        Index('idx_radiology_critical', 'is_critical', 'critical_notified'),
        Index('idx_radiology_report_status', 'report_status', 'status'),
        {'comment': 'Radiology and imaging tests and reports'}
    )
    
    # Validators
    @validates('imaging_type')
    def validate_imaging_type(self, key, value):
        valid_types = [
            'x_ray', 'mri', 'ct_scan', 'ultrasound', 'pet_scan',
            'mammography', 'fluoroscopy', 'bone_scan', 'dexa_scan', 'angiography'
        ]
        if value.lower() not in valid_types:
            raise ValueError(f"Imaging type must be one of: {', '.join(valid_types)}")
        return value.lower()
    
    @validates('category')
    def validate_category(self, key, value):
        valid_categories = ['diagnostic', 'therapeutic', 'interventional', 'screening']
        if value.lower() not in valid_categories:
            raise ValueError(f"Category must be one of: {', '.join(valid_categories)}")
        return value.lower()
    
    @validates('report_status')
    def validate_report_status(self, key, value):
        valid_statuses = ['pending', 'preliminary', 'final', 'addendum', 'amended']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Report status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['ordered', 'scheduled', 'in_progress', 'completed', 'cancelled', 'rejected']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    @validates('priority')
    def validate_priority(self, key, value):
        valid_priorities = ['routine', 'urgent', 'stat']
        if value.lower() not in valid_priorities:
            raise ValueError(f"Priority must be one of: {', '.join(valid_priorities)}")
        return value.lower()
    
    @validates('result_type')
    def validate_result_type(self, key, value):
        if value:
            valid_types = ['normal', 'abnormal', 'critical', 'inconclusive']
            if value.lower() not in valid_types:
                raise ValueError(f"Result type must be one of: {', '.join(valid_types)}")
            return value.lower()
        return value
    
    def __repr__(self) -> str:
        return f"<Radiology(id={self.id}, number='{self.radiology_number}', type='{self.imaging_type}')>"