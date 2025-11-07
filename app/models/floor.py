"""
Floor Model - NEW
Manages building floors for hospital infrastructure
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, CheckConstraint, Index
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional, List

from .base import BaseModel


class Floor(BaseModel):
    """
    Floor model for managing building floors
    Supports multi-floor hospitals with basement levels
    """
    
    __tablename__ = "floors"
    
    # Basic Information
    floor_number: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    floor_name: Mapped[str] = mapped_column(String(100), nullable=False)
    floor_code: Mapped[Optional[str]] = mapped_column(String(20), unique=True, index=True)
    
    # Building Reference
    hospital_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("hospitals.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )
    branch_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("branches.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )
    
    # Floor Details
    total_rooms: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_wards: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_beds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    occupied_beds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Floor Specifications
    square_footage: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Floor Type/Purpose
    floor_type: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        index=True,
        comment="general, icu, operation, emergency, administrative, diagnostic"
    )
    
    # Accessibility Features
    has_elevator: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    has_stairs: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_accessible: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    has_ramp: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Emergency & Safety
    has_emergency_exit: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    fire_extinguishers_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    emergency_assembly_point: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    
    # Additional Features
    has_waiting_area: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    has_restroom: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    has_pantry: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Relationships
    hospital: Mapped[Optional["Hospital"]] = relationship(
        "Hospital",
        back_populates="floors",
        foreign_keys=[hospital_id]
    )
    
    branch: Mapped[Optional["Branch"]] = relationship(
        "Branch",
        back_populates="floors",
        foreign_keys=[branch_id]
    )
    
    rooms: Mapped[List["Room"]] = relationship(
        "Room",
        back_populates="floor",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    wards: Mapped[List["Ward"]] = relationship(
        "Ward",
        back_populates="floor",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    departments: Mapped[List["Department"]] = relationship(
        "Department",
        back_populates="main_floor",
        foreign_keys="Department.main_floor_id",
        lazy="dynamic"
    )
    
    equipment: Mapped[List["Equipment"]] = relationship(
        "Equipment",
        back_populates="floor",
        lazy="dynamic"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('floor_number >= -10 AND floor_number <= 100', name='valid_floor_number'),
        CheckConstraint('total_rooms >= 0', name='positive_total_rooms'),
        CheckConstraint('total_wards >= 0', name='positive_total_wards'),
        CheckConstraint('total_beds >= 0', name='positive_total_beds'),
        CheckConstraint('occupied_beds >= 0', name='positive_occupied_beds'),
        CheckConstraint('occupied_beds <= total_beds', name='occupied_not_exceed_total'),
        CheckConstraint('fire_extinguishers_count >= 0', name='positive_fire_extinguishers'),
        Index('idx_floor_hospital', 'hospital_id', 'floor_number'),
        Index('idx_floor_branch', 'branch_id', 'floor_number'),
        Index('idx_floor_type', 'floor_type'),
        Index('idx_floor_active', 'is_active', 'is_deleted'),
        {'comment': 'Building floors for hospital infrastructure management'}
    )
    
    # Validators
    @validates('floor_number')
    def validate_floor_number(self, key, value):
        """Validate floor number is within acceptable range"""
        if value < -10 or value > 100:
            raise ValueError("Floor number must be between -10 (basement) and 100")
        return value
    
    @validates('floor_type')
    def validate_floor_type(self, key, value):
        """Validate floor type"""
        valid_types = [
            'general', 'icu', 'operation', 'emergency', 
            'administrative', 'diagnostic', 'pharmacy', 
            'laboratory', 'radiology', 'maternity'
        ]
        if value and value.lower() not in valid_types:
            raise ValueError(f"Floor type must be one of: {', '.join(valid_types)}")
        return value.lower() if value else None
    
    @validates('occupied_beds')
    def validate_occupied_beds(self, key, value):
        """Ensure occupied beds don't exceed total beds"""
        if value > self.total_beds:
            raise ValueError("Occupied beds cannot exceed total beds")
        return value
    
    # Properties
    @property
    def display_name(self) -> str:
        """Return formatted floor display name"""
        if self.floor_number == 0:
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
    
    @property
    def available_beds(self) -> int:
        """Calculate available beds"""
        return max(0, self.total_beds - self.occupied_beds)
    
    @property
    def occupancy_rate(self) -> float:
        """Calculate bed occupancy rate percentage"""
        if self.total_beds == 0:
            return 0.0
        return round((self.occupied_beds / self.total_beds) * 100, 2)
    
    @property
    def is_basement(self) -> bool:
        """Check if floor is basement"""
        return self.floor_number < 0
    
    @property
    def is_ground_floor(self) -> bool:
        """Check if floor is ground floor"""
        return self.floor_number == 0
    
    @property
    def is_fully_occupied(self) -> bool:
        """Check if all beds are occupied"""
        return self.occupied_beds >= self.total_beds and self.total_beds > 0
    
    # Methods
    def increment_beds(self, count: int = 1) -> None:
        """Increment occupied beds count"""
        new_count = self.occupied_beds + count
        if new_count > self.total_beds:
            raise ValueError("Cannot exceed total bed capacity")
        self.occupied_beds = new_count
    
    def decrement_beds(self, count: int = 1) -> None:
        """Decrement occupied beds count"""
        new_count = self.occupied_beds - count
        if new_count < 0:
            raise ValueError("Occupied beds cannot be negative")
        self.occupied_beds = new_count
    
    def __repr__(self) -> str:
        """String representation"""
        return f"<Floor(id={self.id}, name='{self.floor_name}', number={self.floor_number}, type='{self.floor_type}')>"
    
