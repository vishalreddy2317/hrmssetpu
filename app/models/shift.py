"""
Shift Model
Work shift definitions
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, Index, CheckConstraint, Time
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional, List

from .base import BaseModel


class Shift(BaseModel):
    """
    Work shift model
    """
    
    __tablename__ = "shifts"
    
    # Shift Details
    shift_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    shift_code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    
    # Timing
    start_time: Mapped[str] = mapped_column(String(10), nullable=False)
    end_time: Mapped[str] = mapped_column(String(10), nullable=False)
    
    # Duration
    duration_hours: Mapped[int] = mapped_column(Integer, nullable=False, comment="in hours")
    
    # Break Time
    break_duration_minutes: Mapped[int] = mapped_column(Integer, default=30, comment="in minutes")
    
    # Shift Type
    shift_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="morning, evening, night, general, rotating"
    )
    
    # Days
    applicable_days: Mapped[Optional[str]] = mapped_column(String(100), comment="JSON array: Mon, Tue, etc.")
    
    # Late/Early Grace Period
    grace_period_minutes: Mapped[int] = mapped_column(Integer, default=15)
    
    # Overtime
    overtime_applicable: Mapped[bool] = mapped_column(Boolean, default=True)
    overtime_rate_multiplier: Mapped[Optional[float]] = mapped_column(Integer, default=1.5)
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='active',
        nullable=False,
        index=True,
        comment="active, inactive"
    )
    
    # Description
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationships
    schedules: Mapped[List["Schedule"]] = relationship(
        "Schedule",
        back_populates="shift",
        lazy="dynamic"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('duration_hours > 0', name='shift_positive_duration'),
        CheckConstraint('break_duration_minutes >= 0', name='shift_positive_break'),
        CheckConstraint('grace_period_minutes >= 0', name='shift_positive_grace'),
        {'comment': 'Work shift definitions'}
    )
    
    # Validators
    @validates('shift_type')
    def validate_shift_type(self, key, value):
        valid_types = ['morning', 'evening', 'night', 'general', 'rotating', 'split']
        if value.lower() not in valid_types:
            raise ValueError(f"Shift type must be one of: {', '.join(valid_types)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['active', 'inactive']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<Shift(id={self.id}, name='{self.shift_name}', time='{self.start_time}-{self.end_time}')>"