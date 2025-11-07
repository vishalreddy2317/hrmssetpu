"""
Room Model - Updated with Floor Reference
Hospital rooms with comprehensive floor location
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional, List
from decimal import Decimal

from .base import BaseModel


class Room(BaseModel):
    """
    Room model with floor reference
    Manages hospital rooms across different floors
    """
    
    __tablename__ = "rooms"
    
    # Basic Information
    room_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    room_name: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Room Type
    room_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        comment="general, private, semi_private, icu, operation, emergency, consultation, observation, isolation"
    )
    
    # ⭐ Floor Reference - NEW
    floor_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("floors.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    floor_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)
    
    # Location
    ward_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("wards.id", ondelete="SET NULL"),
        index=True
    )
    department_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("departments.id", ondelete="SET NULL"),
        index=True
    )
    building: Mapped[Optional[str]] = mapped_column(String(50))
    wing: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Capacity
    bed_capacity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    current_occupancy: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Room Specifications
    size_sqft: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    has_attached_bathroom: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_ac: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_window: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    has_balcony: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_tv: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_telephone: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_refrigerator: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Medical Equipment
    has_oxygen_supply: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_suction: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_monitor: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_ventilator: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Availability
    status: Mapped[str] = mapped_column(
        String(20),
        default='available',
        nullable=False,
        index=True,
        comment="available, occupied, maintenance, reserved, cleaning, under_renovation"
    )
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    is_isolation_room: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Pricing
    price_per_day: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    deposit_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    
    # Additional Info
    description: Mapped[Optional[str]] = mapped_column(Text)
    special_equipment: Mapped[Optional[str]] = mapped_column(Text)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Housekeeping
    last_cleaned_at: Mapped[Optional[str]] = mapped_column(String(50))
    last_maintenance_at: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Relationships
    floor: Mapped[Optional["Floor"]] = relationship(
        "Floor",
        back_populates="rooms",
        foreign_keys=[floor_id]
    )
    
    ward: Mapped[Optional["Ward"]] = relationship(
        "Ward",
        back_populates="rooms"
    )
    
    department: Mapped[Optional["Department"]] = relationship(
        "Department",
        back_populates="rooms"
    )
    
    beds: Mapped[List["Bed"]] = relationship(
        "Bed",
        back_populates="room",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    admissions: Mapped[List["Admission"]] = relationship(
        "Admission",
        back_populates="room",
        lazy="dynamic"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('bed_capacity >= 1', name='room_min_one_bed'),
        CheckConstraint('current_occupancy >= 0', name='room_positive_occupancy'),
        CheckConstraint('current_occupancy <= bed_capacity', name='room_occupancy_not_exceed_capacity'),
        CheckConstraint('size_sqft > 0 OR size_sqft IS NULL', name='room_positive_size'),
        CheckConstraint('price_per_day >= 0 OR price_per_day IS NULL', name='room_positive_price'),
        Index('idx_room_floor', 'floor_id', 'floor_number'),
        Index('idx_room_ward', 'ward_id', 'status'),
        Index('idx_room_department', 'department_id'),
        Index('idx_room_type_status', 'room_type', 'status'),
        Index('idx_room_availability', 'is_available', 'status'),
        {'comment': 'Hospital rooms with floor locations and facilities'}
    )
    
    # Validators
    @validates('room_type')
    def validate_room_type(self, key, value):
        """Validate room type"""
        valid_types = [
            'general', 'private', 'semi_private', 'icu', 'operation',
            'emergency', 'consultation', 'observation', 'isolation',
            'labor', 'recovery', 'nicu', 'pediatric'
        ]
        if value.lower() not in valid_types:
            raise ValueError(f"Room type must be one of: {', '.join(valid_types)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        """Validate status"""
        valid_statuses = [
            'available', 'occupied', 'maintenance', 'reserved',
            'cleaning', 'under_renovation', 'quarantine'
        ]
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    @validates('current_occupancy')
    def validate_current_occupancy(self, key, value):
        """Ensure occupancy doesn't exceed capacity"""
        if value > self.bed_capacity:
            raise ValueError("Current occupancy cannot exceed bed capacity")
        return value
    
    # Properties
    @property
    def available_beds(self) -> int:
        """Calculate available beds"""
        return max(0, self.bed_capacity - self.current_occupancy)
    
    @property
    def is_full(self) -> bool:
        """Check if room is at full capacity"""
        return self.current_occupancy >= self.bed_capacity
    
    @property
    def occupancy_rate(self) -> float:
        """Calculate occupancy percentage"""
        if self.bed_capacity == 0:
            return 0.0
        return round((self.current_occupancy / self.bed_capacity) * 100, 2)
    
    @property
    def floor_display(self) -> str:
        """Get floor display name"""
        if self.floor_number is None:
            return "N/A"
        elif self.floor_number == 0:
            return "Ground Floor"
        elif self.floor_number < 0:
            return f"Basement {abs(self.floor_number)}"
        elif self.floor_number == 1:
            return "1st Floor"
        elif self.floor_number == 2:
            return "2nd Floor"
        elif self.floor_number == 3:
            return "3rd Floor"
        else:
            return f"{self.floor_number}th Floor"
    
    def __repr__(self) -> str:
        floor_info = f", floor={self.floor_number}" if self.floor_number is not None else ""
        return f"<Room(id={self.id}, number='{self.room_number}'{floor_info}, type='{self.room_type}')>"
