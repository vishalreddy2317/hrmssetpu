"""
Imaging Model
Radiology and imaging services (X-Ray, CT, MRI, Ultrasound)
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional
from decimal import Decimal

from .base import BaseModel


class Imaging(BaseModel):
    """
    Medical imaging and radiology model
    """
    
    __tablename__ = "imagings"
    
    # Imaging Details
    imaging_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    
    # Patient
    patient_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Ordering Doctor
    ordered_by_doctor_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("doctors.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Imaging Type
    imaging_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        comment="xray, ct_scan, mri, ultrasound, mammography, pet_scan, fluoroscopy"
    )
    
    # Body Part/Region
    body_part: Mapped[str] = mapped_column(String(100), nullable=False)
    study_description: Mapped[str] = mapped_column(String(200), nullable=False)
    
    # Modality
    modality: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Scheduling
    order_date: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    order_time: Mapped[str] = mapped_column(String(10), nullable=False)
    scheduled_date: Mapped[Optional[str]] = mapped_column(String(20), index=True)
    scheduled_time: Mapped[Optional[str]] = mapped_column(String(10))
    
    # Actual Timing
    actual_date: Mapped[Optional[str]] = mapped_column(String(20))
    actual_time: Mapped[Optional[str]] = mapped_column(String(10))
    
    # Priority
    priority: Mapped[str] = mapped_column(
        String(20),
        default='routine',
        nullable=False,
        comment="stat, urgent, routine"
    )
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='pending',
        nullable=False,
        index=True,
        comment="pending, scheduled, in_progress, completed, cancelled, reported"
    )
    
    # Clinical Information
    clinical_indication: Mapped[str] = mapped_column(Text, nullable=False)
    relevant_history: Mapped[Optional[str]] = mapped_column(Text)
    
    # Technician
    performed_by: Mapped[Optional[str]] = mapped_column(String(200))
    technician_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("staffs.id", ondelete="SET NULL")
    )
    
    # Radiologist
    radiologist_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("doctors.id", ondelete="SET NULL")
    )
    reported_by: Mapped[Optional[str]] = mapped_column(String(200))
    report_date: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Findings
    findings: Mapped[Optional[str]] = mapped_column(Text)
    impression: Mapped[Optional[str]] = mapped_column(Text)
    recommendations: Mapped[Optional[str]] = mapped_column(Text)
    
    # Contrast
    contrast_used: Mapped[bool] = mapped_column(Boolean, default=False)
    contrast_type: Mapped[Optional[str]] = mapped_column(String(100))
    contrast_amount: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Radiation (for X-Ray, CT)
    radiation_dose: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Images
    image_count: Mapped[Optional[int]] = mapped_column(Integer)
    images_urls: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array of image URLs")
    dicom_study_id: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Report
    report_url: Mapped[Optional[str]] = mapped_column(String(500))
    is_abnormal: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Cost
    cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    
    # Location
    imaging_center: Mapped[Optional[str]] = mapped_column(String(200))
    imaging_floor: Mapped[Optional[int]] = mapped_column(Integer)  # ⭐ Floor reference
    
    # Patient Preparation
    preparation_instructions: Mapped[Optional[str]] = mapped_column(Text)
    fasting_required: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Quality
    image_quality: Mapped[Optional[str]] = mapped_column(String(20), comment="excellent, good, adequate, poor")
    
    # Notes
    notes: Mapped[Optional[str]] = mapped_column(Text)
    technician_notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationships
    patient: Mapped["Patient"] = relationship(
        "Patient",
        backref="imaging_studies"
    )
    
    ordered_by: Mapped["Doctor"] = relationship(
        "Doctor",
        foreign_keys=[ordered_by_doctor_id],
        backref="ordered_imaging_studies"
    )
    
    radiologist: Mapped[Optional["Doctor"]] = relationship(
        "Doctor",
        foreign_keys=[radiologist_id],
        backref="reported_imaging_studies"
    )
    
    technician: Mapped[Optional["Staff"]] = relationship(
        "Staff",
        backref="performed_imaging_studies"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('cost >= 0 OR cost IS NULL', name='imaging_positive_cost'),
        CheckConstraint('image_count >= 0 OR image_count IS NULL', name='imaging_positive_image_count'),
        Index('idx_imaging_patient', 'patient_id', 'order_date'),
        Index('idx_imaging_type', 'imaging_type', 'status'),
        Index('idx_imaging_priority', 'priority', 'status'),
        Index('idx_imaging_scheduled', 'scheduled_date', 'status'),
        {'comment': 'Medical imaging and radiology services'}
    )
    
    # Validators
    @validates('imaging_type')
    def validate_imaging_type(self, key, value):
        valid_types = [
            'xray', 'ct_scan', 'mri', 'ultrasound', 'mammography',
            'pet_scan', 'fluoroscopy', 'dexa_scan', 'echocardiogram'
        ]
        if value.lower() not in valid_types:
            raise ValueError(f"Imaging type must be one of: {', '.join(valid_types)}")
        return value.lower()
    
    @validates('priority')
    def validate_priority(self, key, value):
        valid_priorities = ['stat', 'urgent', 'routine']
        if value.lower() not in valid_priorities:
            raise ValueError(f"Priority must be one of: {', '.join(valid_priorities)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['pending', 'scheduled', 'in_progress', 'completed', 'cancelled', 'reported']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<Imaging(id={self.id}, number='{self.imaging_number}', type='{self.imaging_type}', status='{self.status}')>"