"""
Lab Report Model
Laboratory test results and reports
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional

from .base import BaseModel


class LabReport(BaseModel):
    """
    Laboratory test report model
    """
    
    __tablename__ = "lab_reports"
    
    # Report Details
    report_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    
    # Test Reference
    lab_test_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("lab_tests.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True
    )
    
    # Patient
    patient_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Report Details
    report_date: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    report_time: Mapped[str] = mapped_column(String(10), nullable=False)
    
    # Results
    test_results: Mapped[str] = mapped_column(Text, nullable=False, comment="JSON format with test parameters")
    interpretation: Mapped[Optional[str]] = mapped_column(Text)
    findings: Mapped[Optional[str]] = mapped_column(Text)
    
    # Status
    result_status: Mapped[str] = mapped_column(
        String(20),
        default='normal',
        nullable=False,
        index=True,
        comment="normal, abnormal, critical, inconclusive"
    )
    
    # Staff
    tested_by: Mapped[Optional[str]] = mapped_column(String(200))
    verified_by: Mapped[Optional[str]] = mapped_column(String(200))
    approved_by_doctor_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("doctors.id", ondelete="SET NULL")
    )
    
    # Reference Values
    reference_ranges: Mapped[Optional[str]] = mapped_column(Text, comment="JSON format")
    
    # Notes
    technician_notes: Mapped[Optional[str]] = mapped_column(Text)
    doctor_notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Attachments
    report_file_url: Mapped[Optional[str]] = mapped_column(String(500))
    images_urls: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array of image URLs")
    
    # Critical Value Alert
    is_critical: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    critical_value_notified: Mapped[bool] = mapped_column(Boolean, default=False)
    notified_at: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Quality Control
    quality_check_passed: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    quality_check_notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationships
    lab_test: Mapped["LabTest"] = relationship(
        "LabTest",
        back_populates="lab_report"
    )
    
    patient: Mapped["Patient"] = relationship(
        "Patient",
        backref="lab_reports"
    )
    
    approved_by: Mapped[Optional["Doctor"]] = relationship(
        "Doctor",
        backref="approved_lab_reports"
    )
    
    # Table Arguments
    __table_args__ = (
        Index('idx_labreport_patient', 'patient_id', 'report_date'),
        Index('idx_labreport_status', 'result_status', 'is_critical'),
        {'comment': 'Laboratory test results and reports'}
    )
    
    # Validators
    @validates('result_status')
    def validate_result_status(self, key, value):
        valid_statuses = ['normal', 'abnormal', 'critical', 'inconclusive', 'pending_review']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Result status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<LabReport(id={self.id}, number='{self.report_number}', status='{self.result_status}')>"