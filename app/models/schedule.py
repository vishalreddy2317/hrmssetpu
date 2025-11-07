"""
Schedule Model
Staff work schedule and roster
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional

from .base import BaseModel


class Schedule(BaseModel):
    """
    Staff schedule/roster model
    """
    
    __tablename__ = "schedules"
    
    # Schedule Details
    schedule_date: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    
    # Doctor
    doctor_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("doctors.id", ondelete="CASCADE"),
        index=True
    )
    
    # Shift
    shift_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("shifts.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Department
    department_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("departments.id", ondelete="SET NULL")
    )
    
    # Timing (can override shift timings)
    start_time: Mapped[Optional[str]] = mapped_column(String(10))
    end_time: Mapped[Optional[str]] = mapped_column(String(10))
    
    # Availability
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    max_appointments: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='scheduled',
        nullable=False,
        index=True,
        comment="scheduled, completed, cancelled, on_leave"
    )
    
    # Day Type
    day_type: Mapped[str] = mapped_column(
        String(20),
        default='working',
        nullable=False,
        comment="working, holiday, weekend, on_call"
    )
    
    # On-Call
    is_on_call: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Notes
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationships
    doctor: Mapped[Optional["Doctor"]] = relationship(
        "Doctor",
        back_populates="schedules"
    )
    
    shift: Mapped["Shift"] = relationship(
        "Shift",
        back_populates="schedules"
    )
    
    department: Mapped[Optional["Department"]] = relationship(
        "Department",
        backref="schedules"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('max_appointments >= 0 OR max_appointments IS NULL', name='schedule_positive_max_appointments'),
        Index('idx_schedule_doctor_date', 'doctor_id', 'schedule_date'),
        Index('idx_schedule_shift', 'shift_id', 'schedule_date'),
        Index('idx_schedule_date_status', 'schedule_date', 'status'),
        {'comment': 'Staff work schedules and rosters'}
    )
    
    # Validators
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['scheduled', 'completed', 'cancelled', 'on_leave', 'rescheduled']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    @validates('day_type')
    def validate_day_type(self, key, value):
        valid_types = ['working', 'holiday', 'weekend', 'on_call']
        if value.lower() not in valid_types:
            raise ValueError(f"Day type must be one of: {', '.join(valid_types)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<Schedule(id={self.id}, date='{self.schedule_date}', doctor_id={self.doctor_id})>"