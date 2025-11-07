"""
Attendance Model
Staff attendance tracking and management
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint, Time
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional

from .base import BaseModel


class Attendance(BaseModel):
    """
    Staff attendance model
    """
    
    __tablename__ = "attendances"
    
    # Attendance Details
    attendance_date: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    
    # Staff Reference (can be doctor, nurse, or staff)
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
    
    # Employee Info (denormalized for quick access)
    employee_name: Mapped[str] = mapped_column(String(200), nullable=False)
    employee_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    
    # Timing
    check_in_time: Mapped[Optional[str]] = mapped_column(String(10))
    check_out_time: Mapped[Optional[str]] = mapped_column(String(10))
    
    # Work Hours
    scheduled_hours: Mapped[Optional[int]] = mapped_column(Integer, comment="in minutes")
    actual_hours: Mapped[Optional[int]] = mapped_column(Integer, comment="in minutes")
    overtime_hours: Mapped[Optional[int]] = mapped_column(Integer, default=0, comment="in minutes")
    
    # Shift
    shift_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("shifts.id", ondelete="SET NULL")
    )
    shift_name: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
        comment="present, absent, half_day, on_leave, late, early_departure, holiday"
    )
    
    # Late/Early
    is_late: Mapped[bool] = mapped_column(Boolean, default=False)
    late_by_minutes: Mapped[Optional[int]] = mapped_column(Integer)
    is_early_departure: Mapped[bool] = mapped_column(Boolean, default=False)
    early_by_minutes: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Location (if biometric/GPS based)
    check_in_location: Mapped[Optional[str]] = mapped_column(String(200))
    check_out_location: Mapped[Optional[str]] = mapped_column(String(200))
    
    # Device/Method
    check_in_method: Mapped[Optional[str]] = mapped_column(String(50), comment="biometric, manual, rfid, mobile_app")
    check_out_method: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Break Time
    total_break_minutes: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    
    # Approval
    approved_by: Mapped[Optional[str]] = mapped_column(String(200))
    approval_date: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Notes
    notes: Mapped[Optional[str]] = mapped_column(Text)
    remarks: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationships
    staff: Mapped[Optional["Staff"]] = relationship(
        "Staff",
        back_populates="attendances"
    )
    
    doctor: Mapped[Optional["Doctor"]] = relationship(
        "Doctor",
        backref="attendances"
    )
    
    nurse: Mapped[Optional["Nurse"]] = relationship(
        "Nurse",
        backref="attendances"
    )
    
    shift: Mapped[Optional["Shift"]] = relationship(
        "Shift",
        backref="attendances"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('overtime_hours >= 0', name='attendance_positive_overtime'),
        CheckConstraint('late_by_minutes >= 0 OR late_by_minutes IS NULL', name='attendance_positive_late_minutes'),
        CheckConstraint('early_by_minutes >= 0 OR early_by_minutes IS NULL', name='attendance_positive_early_minutes'),
        Index('idx_attendance_date', 'attendance_date', 'status'),
        Index('idx_attendance_employee', 'employee_id', 'attendance_date'),
        Index('idx_attendance_staff', 'staff_id', 'attendance_date'),
        Index('idx_attendance_doctor', 'doctor_id', 'attendance_date'),
        Index('idx_attendance_nurse', 'nurse_id', 'attendance_date'),
        {'comment': 'Staff attendance tracking and management'}
    )
    
    # Validators
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = [
            'present', 'absent', 'half_day', 'on_leave',
            'late', 'early_departure', 'holiday', 'weekend'
        ]
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<Attendance(id={self.id}, employee='{self.employee_name}', date='{self.attendance_date}', status='{self.status}')>"