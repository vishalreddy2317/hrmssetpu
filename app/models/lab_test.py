"""
Lab Test Model
Laboratory test orders and tracking
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional, List
from decimal import Decimal

from .base import BaseModel


class LabTest(BaseModel):
    """
    Laboratory test order model
    """
    
    __tablename__ = "lab_tests"
    
    # Test Details
    test_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    test_name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    test_code: Mapped[Optional[str]] = mapped_column(String(50), index=True)
    
    # Patient and Doctor
    patient_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    ordered_by_doctor_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("doctors.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Test Category
    test_category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        comment="blood, urine, stool, imaging, pathology, microbiology, biochemistry"
    )
    
    # Test Type
    test_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="routine, urgent, stat, fasting, culture, biopsy"
    )
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='pending',
        nullable=False,
        index=True,
        comment="pending, sample_collected, in_progress, completed, cancelled, rejected"
    )
    
    # Dates and Times
    order_date: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    order_time: Mapped[str] = mapped_column(String(10), nullable=False)
    sample_collection_date: Mapped[Optional[str]] = mapped_column(String(20))
    sample_collection_time: Mapped[Optional[str]] = mapped_column(String(10))
    report_date: Mapped[Optional[str]] = mapped_column(String(20))
    report_time: Mapped[Optional[str]] = mapped_column(String(10))
    
    # Sample Details
    sample_type: Mapped[Optional[str]] = mapped_column(String(50), comment="blood, serum, plasma, urine, etc.")
    sample_id: Mapped[Optional[str]] = mapped_column(String(50), unique=True, index=True)
    sample_collected_by: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Priority
    priority: Mapped[str] = mapped_column(
        String(20),
        default='routine',
        nullable=False,
        index=True,
        comment="routine, urgent, stat"
    )
    
    # Instructions
    special_instructions: Mapped[Optional[str]] = mapped_column(Text)
    fasting_required: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Cost
    test_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    
    # Notes
    clinical_notes: Mapped[Optional[str]] = mapped_column(Text)
    rejection_reason: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationships
    patient: Mapped["Patient"] = relationship(
        "Patient",
        back_populates="lab_tests"
    )
    
    ordered_by: Mapped["Doctor"] = relationship(
        "Doctor",
        backref="ordered_lab_tests"
    )
    
    lab_report: Mapped[Optional["LabReport"]] = relationship(
        "LabReport",
        back_populates="lab_test",
        uselist=False
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('test_cost >= 0 OR test_cost IS NULL', name='labtest_positive_cost'),
        Index('idx_labtest_patient', 'patient_id', 'status'),
        Index('idx_labtest_doctor', 'ordered_by_doctor_id'),
        Index('idx_labtest_order_date', 'order_date', 'priority'),
        Index('idx_labtest_category', 'test_category', 'status'),
        {'comment': 'Laboratory test orders and tracking'}
    )
    
    # Validators
    @validates('test_category')
    def validate_test_category(self, key, value):
        valid_categories = [
            'blood', 'urine', 'stool', 'imaging', 'pathology',
            'microbiology', 'biochemistry', 'hematology', 'serology'
        ]
        if value.lower() not in valid_categories:
            raise ValueError(f"Test category must be one of: {', '.join(valid_categories)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = [
            'pending', 'sample_collected', 'in_progress',
            'completed', 'cancelled', 'rejected'
        ]
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    @validates('priority')
    def validate_priority(self, key, value):
        valid_priorities = ['routine', 'urgent', 'stat']
        if value.lower() not in valid_priorities:
            raise ValueError(f"Priority must be one of: {', '.join(valid_priorities)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<LabTest(id={self.id}, number='{self.test_number}', name='{self.test_name}', status='{self.status}')>"