"""
Ward Model - Updated with Floor Reference
Hospital wards with floor location
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional, List

from .base import BaseModel


class Ward(BaseModel):
    """
    Ward model with floor reference
    Manages hospital wards across different floors
    """
    
    __tablename__ = "wards"
    
    # Basic Information
    ward_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    ward_code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    
    # Ward Type
    ward_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        comment="general, icu, nicu, picu, pediatric, maternity, isolation, burns, cardiac"
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
    department_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("departments.id", ondelete="SET NULL"),
        index=True
    )
    building: Mapped[Optional[str]] = mapped_column(String(50))
    wing: Mapped[Optional[str]] = mapped_column(String(50), comment="East, West, North, South, Central")
    section: Mapped[Optional[str]] = mapped_column(String(50), comment="A, B, C, etc.")
    
    # Capacity
    total_beds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    occupied_beds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    reserved_beds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_rooms: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Staff Assignment
    head_nurse_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("nurses.id", ondelete="SET NULL")
    )
    total_nurses: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_staff: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Facilities
    has_isolation_room: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_emergency_equipment: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    has_nurse_station: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    has_waiting_area: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    has_oxygen_supply: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    has_ventilators: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    ventilator_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Contact
    contact_number: Mapped[Optional[str]] = mapped_column(String(20))
    extension: Mapped[Optional[str]] = mapped_column(String(10))
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='active',
        nullable=False,
        index=True,
        comment="active, inactive, maintenance, under_renovation"
    )
    
    # Additional Info
    description: Mapped[Optional[str]] = mapped_column(Text)
    special_notes: Mapped[Optional[str]] = mapped_column(Text)
    infection_control_level: Mapped[Optional[str]] = mapped_column(
        String(20),
        comment="standard, enhanced, strict"
    )
    
    # Relationships
    floor: Mapped[Optional["Floor"]] = relationship(
        "Floor",
        back_populates="wards",
        foreign_keys=[floor_id]
    )
    
    department: Mapped[Optional["Department"]] = relationship(
        "Department",
        back_populates="wards"
    )
    
    head_nurse: Mapped[Optional["Nurse"]] = relationship(
        "Nurse",
        back_populates="wards_managed",
        foreign_keys=[head_nurse_id]
    )
    
    rooms: Mapped[List["Room"]] = relationship(
        "Room",
        back_populates="ward",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    beds: Mapped[List["Bed"]] = relationship(
        "Bed",
        back_populates="ward",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    admissions: Mapped[List["Admission"]] = relationship(
        "Admission",
        back_populates="ward",
        lazy="dynamic"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('total_beds >= 0', name='ward_positive_total_beds'),
        CheckConstraint('occupied_beds >= 0', name='ward_positive_occupied_beds'),
        CheckConstraint('reserved_beds >= 0', name='ward_positive_reserved_beds'),
        CheckConstraint('occupied_beds <= total_beds', name='ward_occupied_not_exceed_total'),
        CheckConstraint('reserved_beds <= total_beds', name='ward_reserved_not_exceed_total'),
        CheckConstraint('ventilator_count >= 0', name='ward_positive_ventilators'),
        Index('idx_ward_floor', 'floor_id', 'floor_number'),
        Index('idx_ward_department', 'department_id', 'status'),
        Index('idx_ward_type_status', 'ward_type', 'status'),
        {'comment': 'Hospital wards with floor locations'}
    )
    
    # Validators
    @validates('ward_type')
    def validate_ward_type(self, key, value):
        """Validate ward type"""
        valid_types = [
            'general', 'icu', 'nicu', 'picu', 'pediatric', 'maternity',
            'isolation', 'burns', 'cardiac', 'oncology', 'orthopedic',
            'neurology', 'surgical', 'medical', 'psychiatric'
        ]
        if value.lower() not in valid_types:
            raise ValueError(f"Ward type must be one of: {', '.join(valid_types)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        """Validate status"""
        valid_statuses = ['active', 'inactive', 'maintenance', 'under_renovation', 'closed']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    @validates('occupied_beds')
    def validate_occupied_beds(self, key, value):
        """Ensure occupied beds don't exceed total"""
        if value > self.total_beds:
            raise ValueError("Occupied beds cannot exceed total beds")
        return value
    
    # Properties
    @property
    def available_beds(self) -> int:
        """Calculate available beds"""
        return max(0, self.total_beds - self.occupied_beds - self.reserved_beds)
    
    @property
    def occupancy_rate(self) -> float:
        """Calculate occupancy percentage"""
        if self.total_beds == 0:
            return 0.0
        return round((self.occupied_beds / self.total_beds) * 100, 2)
    
    @property
    def is_full(self) -> bool:
        """Check if ward is at full capacity"""
        return self.available_beds == 0
    
    @property
    def is_critical_care(self) -> bool:
        """Check if ward is critical care unit"""
        return self.ward_type in ['icu', 'nicu', 'picu', 'cardiac']
    
    def __repr__(self) -> str:
        floor_info = f", floor={self.floor_number}" if self.floor_number is not None else ""
        return f"<Ward(id={self.id}, name='{self.ward_name}', type='{self.ward_type}'{floor_info})>"
    