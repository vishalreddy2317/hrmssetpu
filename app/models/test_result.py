"""
Test Result Model
Detailed laboratory test results with parameters
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional
from decimal import Decimal

from .base import BaseModel


class TestResult(BaseModel):
    """
    Detailed test result model for lab tests
    """
    
    __tablename__ = "test_results"
    
    # Result Details
    result_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    
    # Patient and Test References
    patient_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    lab_test_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("lab_tests.id", ondelete="SET NULL"),
        index=True
    )
    doctor_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("doctors.id", ondelete="SET NULL"),
        index=True
    )
    
    # Test Information
    test_name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    test_code: Mapped[Optional[str]] = mapped_column(String(50), index=True)
    parameter_name: Mapped[str] = mapped_column(String(200), nullable=False)
    parameter_code: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Result Values
    result_value: Mapped[str] = mapped_column(String(200), nullable=False)
    result_value_numeric: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 4))
    result_unit: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Normal Range
    normal_range_min: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 4))
    normal_range_max: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 4))
    normal_range_text: Mapped[Optional[str]] = mapped_column(String(200))
    reference_range: Mapped[Optional[str]] = mapped_column(String(200))
    
    # Status
    result_status: Mapped[str] = mapped_column(
        String(20),
        default='normal',
        nullable=False,
        index=True,
        comment="normal, abnormal, high, low, critical"
    )
    
    # Flags
    is_abnormal: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_critical: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    is_panic_value: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Interpretation
    interpretation: Mapped[Optional[str]] = mapped_column(Text)
    clinical_significance: Mapped[Optional[str]] = mapped_column(Text)
    
    # Sample Details
    sample_type: Mapped[Optional[str]] = mapped_column(
        String(50),
        comment="blood, serum, plasma, urine, stool, csf, etc."
    )
    sample_id: Mapped[Optional[str]] = mapped_column(String(50), index=True)
    sample_collected_date: Mapped[Optional[str]] = mapped_column(String(20))
    sample_collected_time: Mapped[Optional[str]] = mapped_column(String(10))
    
    # Testing Details
    test_date: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    test_time: Mapped[str] = mapped_column(String(10), nullable=False)
    
    tested_by: Mapped[Optional[str]] = mapped_column(String(200))
    technician_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("technicians.id", ondelete="SET NULL")
    )
    
    # Verification
    verified_by: Mapped[Optional[str]] = mapped_column(String(200))
    verified_at: Mapped[Optional[str]] = mapped_column(String(50))
    
    approved_by: Mapped[Optional[str]] = mapped_column(String(200))
    approved_at: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Method and Equipment
    test_method: Mapped[Optional[str]] = mapped_column(String(200))
    equipment_used: Mapped[Optional[str]] = mapped_column(String(200))
    
    # Quality Control
    quality_check_passed: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    quality_check_notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Comments
    technician_comments: Mapped[Optional[str]] = mapped_column(Text)
    doctor_comments: Mapped[Optional[str]] = mapped_column(Text)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Delta Check (comparison with previous results)
    previous_result_value: Mapped[Optional[str]] = mapped_column(String(200))
    delta_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 4))
    delta_percentage: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    
    # Relationships
    patient: Mapped["Patient"] = relationship(
        "Patient",
        backref="test_results"
    )
    
    lab_test: Mapped[Optional["LabTest"]] = relationship(
        "LabTest",
        backref="detailed_results"
    )
    
    doctor: Mapped[Optional["Doctor"]] = relationship(
        "Doctor",
        backref="reviewed_test_results"
    )
    
    technician: Mapped[Optional["Technician"]] = relationship(
        "Technician",
        backref="test_results_performed"
    )
    
    # Table Arguments
    __table_args__ = (
        Index('idx_testresult_patient', 'patient_id', 'test_date'),
        Index('idx_testresult_lab_test', 'lab_test_id', 'parameter_name'),
        Index('idx_testresult_status', 'result_status', 'is_critical'),
        Index('idx_testresult_test_name', 'test_name', 'parameter_name'),
        {'comment': 'Detailed laboratory test results with parameters'}
    )
    
    # Validators
    @validates('result_status')
    def validate_result_status(self, key, value):
        valid = ['normal', 'abnormal', 'high', 'low', 'critical', 'borderline']
        if value.lower() not in valid:
            raise ValueError(f"Result status must be one of: {', '.join(valid)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<TestResult(id={self.id}, test='{self.test_name}', parameter='{self.parameter_name}')>"