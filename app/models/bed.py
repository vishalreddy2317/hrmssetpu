"""
Bed Model
Individual bed management within rooms
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional
from decimal import Decimal

from .base import BaseModel


class Bed(BaseModel):
    """
    Bed model for individual bed tracking
    """
    
    __tablename__ = "beds"
    
    # Basic Information
    bed_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    bed_code: Mapped[Optional[str]] = mapped_column(String(20), unique=True, index=True)
    
    # Location
    room_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("rooms.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    ward_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("wards.id", ondelete="SET NULL"),
        index=True
    )
    
    # Bed Type
    bed_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        comment="general, icu, electric, manual, pediatric, maternity, bariatric"
    )
    
    # Specifications
    is_electric: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_side_rails: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_adjustable: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    weight_capacity_kg: Mapped[Optional[Decimal]] = mapped_column(Numeric(6, 2))
    
    # Equipment
    has_iv_stand: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_oxygen_port: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_suction_port: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_monitor: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='available',
        nullable=False,
        index=True,
        comment="available, occupied, maintenance, reserved, cleaning"
    )
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    
    # Current Assignment
    current_patient_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("patients.id", ondelete="SET NULL"),
        index=True
    )
    assigned_at: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Maintenance
    last_maintenance_date: Mapped[Optional[str]] = mapped_column(String(50))
    next_maintenance_date: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Additional Info
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationships
    room: Mapped["Room"] = relationship(
        "Room",
        back_populates="beds"
    )
    
    ward: Mapped[Optional["Ward"]] = relationship(
        "Ward",
        back_populates="beds"
    )
    
    current_patient: Mapped[Optional["Patient"]] = relationship(
        "Patient",
        back_populates="current_bed",
        foreign_keys=[current_patient_id]
    )
    
    admissions: Mapped[List["Admission"]] = relationship(
        "Admission",
        back_populates="bed",
        lazy="dynamic"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('weight_capacity_kg > 0 OR weight_capacity_kg IS NULL', name='bed_positive_weight_capacity'),
        Index('idx_bed_room', 'room_id', 'status'),
        Index('idx_bed_ward', 'ward_id', 'status'),
        Index('idx_bed_availability', 'is_available', 'status'),
        Index('idx_bed_patient', 'current_patient_id'),
        {'comment': 'Individual bed tracking and management'}
    )
    
    # Validators
    @validates('bed_type')
    def validate_bed_type(self, key, value):
        """Validate bed type"""
        valid_types = [
            'general', 'icu', 'electric', 'manual', 'pediatric',
            'maternity', 'bariatric', 'orthopedic', 'psychiatric'
        ]
        if value.lower() not in valid_types:
            raise ValueError(f"Bed type must be one of: {', '.join(valid_types)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        """Validate status"""
        valid_statuses = ['available', 'occupied', 'maintenance', 'reserved', 'cleaning', 'out_of_service']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    # Methods
    def assign_patient(self, patient_id: int) -> None:
        """Assign bed to patient"""
        from datetime import datetime
        self.current_patient_id = patient_id
        self.status = 'occupied'
        self.is_available = False
        self.assigned_at = datetime.utcnow().isoformat()
    
    def release_bed(self) -> None:
        """Release bed from patient"""
        self.current_patient_id = None
        self.status = 'available'
        self.is_available = True
        self.assigned_at = None
    
    def __repr__(self) -> str:
        return f"<Bed(id={self.id}, number='{self.bed_number}', status='{self.status}')>"
