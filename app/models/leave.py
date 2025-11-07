"""
Leave Model
Staff leave request and management
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional

from .base import BaseModel


class Leave(BaseModel):
    """
    Leave request model
    """
    
    __tablename__ = "leaves"
    
    # Leave Details
    leave_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    
    # Staff Reference
    staff_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("staffs.id", ondelete="CASCADE"),
        index=True
    )
    doctor_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("doctors.id", ondelete="CASCADE"),
        index=True
    )
    nurse_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("nurses.id", ondelete="CASCADE"),
        index=True
    )
    
    # Employee Info
    employee_name: Mapped[str] = mapped_column(String(200), nullable=False)
    employee_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    
    # Leave Type
    leave_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        comment="sick, casual, earned, maternity, paternity, unpaid, compensatory, bereavement"
    )
    
    # Duration
    start_date: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    end_date: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    total_days: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Half Day
    is_half_day: Mapped[bool] = mapped_column(Boolean, default=False)
    half_day_session: Mapped[Optional[str]] = mapped_column(String(20), comment="first_half, second_half")
    
    # Reason
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Application Date
    application_date: Mapped[str] = mapped_column(String(20), nullable=False)
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='pending',
        nullable=False,
        index=True,
        comment="pending, approved, rejected, cancelled"
    )
    
    # Approval
    approved_by: Mapped[Optional[str]] = mapped_column(String(200))
    approval_date: Mapped[Optional[str]] = mapped_column(String(20))
    approval_remarks: Mapped[Optional[str]] = mapped_column(Text)
    
    # Rejection
    rejected_by: Mapped[Optional[str]] = mapped_column(String(200))
    rejection_date: Mapped[Optional[str]] = mapped_column(String(20))
    rejection_reason: Mapped[Optional[str]] = mapped_column(Text)
    
    # Supporting Documents
    attachment_url: Mapped[Optional[str]] = mapped_column(String(500))
    medical_certificate_url: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Contact During Leave
    contact_number: Mapped[Optional[str]] = mapped_column(String(20))
    emergency_contact: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Handover
    handover_to: Mapped[Optional[str]] = mapped_column(String(200))
    handover_notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Notes
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationships
    staff: Mapped[Optional["Staff"]] = relationship(
        "Staff",
        back_populates="leaves"
    )
    
    doctor: Mapped[Optional["Doctor"]] = relationship(
        "Doctor",
        backref="leaves"
    )
    
    nurse: Mapped[Optional["Nurse"]] = relationship(
        "Nurse",
        backref="leaves"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('total_days > 0', name='leave_positive_days'),
        Index('idx_leave_employee', 'employee_id', 'start_date'),
        Index('idx_leave_dates', 'start_date', 'end_date'),
        Index('idx_leave_type_status', 'leave_type', 'status'),
        {'comment': 'Staff leave requests and management'}
    )
    
    # Validators
    @validates('leave_type')
    def validate_leave_type(self, key, value):
        valid_types = [
            'sick', 'casual', 'earned', 'maternity', 'paternity',
            'unpaid', 'compensatory', 'bereavement', 'study', 'sabbatical'
        ]
        if value.lower() not in valid_types:
            raise ValueError(f"Leave type must be one of: {', '.join(valid_types)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['pending', 'approved', 'rejected', 'cancelled', 'withdrawn']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<Leave(id={self.id}, number='{self.leave_number}', employee='{self.employee_name}', type='{self.leave_type}')>"