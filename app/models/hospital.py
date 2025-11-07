"""
Hospital Model - Updated with Floor Support
Main hospital entity with multi-floor building support
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, Numeric, CheckConstraint, Index
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional, List
import re

from .base import BaseModel


class Hospital(BaseModel):
    """
    Hospital model - main entity
    Manages hospital information with floor infrastructure
    """
    
    __tablename__ = "hospitals"
    
    # Basic Information
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    registration_number: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
    
    # Hospital Type
    hospital_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        comment="general, specialized, clinic, multi_specialty, teaching, trauma_center"
    )
    
    # Location
    address: Mapped[str] = mapped_column(Text, nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    state: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    country: Mapped[str] = mapped_column(String(100), nullable=False, default="USA")
    pincode: Mapped[str] = mapped_column(String(20), nullable=False)
    latitude: Mapped[Optional[Numeric]] = mapped_column(Numeric(10, 8), nullable=True)
    longitude: Mapped[Optional[Numeric]] = mapped_column(Numeric(11, 8), nullable=True)
    
    # Contact Information
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    website: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    emergency_phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    
    # ⭐ Building Details - UPDATED
    total_floors: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    basement_floors: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_buildings: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    total_area_sqft: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Capacity
    total_beds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_rooms: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_wards: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    icu_beds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    emergency_beds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    operation_theaters: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Staff Count
    total_doctors: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_nurses: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_staff: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Facilities
    has_emergency: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    has_ambulance: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    has_blood_bank: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_pharmacy: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    has_laboratory: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    has_radiology: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    has_icu: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    has_nicu: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_dialysis: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_mortuary: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    has_cafeteria: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    has_parking: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Accreditation & Licensing
    accreditation: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    accreditation_body: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    license_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    license_expiry_date: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default='active', nullable=False, index=True)
    is_24x7: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_government: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Additional Information
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    established_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    specializations: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relationships
    floors: Mapped[List["Floor"]] = relationship(
        "Floor",
        back_populates="hospital",
        cascade="all, delete-orphan",
        lazy="dynamic",
        foreign_keys="Floor.hospital_id"
    )
    
    branches: Mapped[List["Branch"]] = relationship(
        "Branch",
        back_populates="hospital",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    departments: Mapped[List["Department"]] = relationship(
        "Department",
        back_populates="hospital",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    doctors: Mapped[List["Doctor"]] = relationship(
        "Doctor",
        back_populates="hospital",
        lazy="dynamic"
    )
    
    nurses: Mapped[List["Nurse"]] = relationship(
        "Nurse",
        back_populates="hospital",
        lazy="dynamic"
    )
    
    patients: Mapped[List["Patient"]] = relationship(
        "Patient",
        back_populates="hospital",
        lazy="dynamic"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('total_floors >= 1', name='min_one_floor'),
        CheckConstraint('basement_floors >= 0', name='positive_basement_floors'),
        CheckConstraint('total_beds >= 0', name='positive_total_beds'),
        CheckConstraint('total_rooms >= 0', name='positive_total_rooms'),
        CheckConstraint('established_year >= 1800 AND established_year <= 2100', name='valid_established_year'),
        Index('idx_hospital_location', 'city', 'state', 'country'),
        Index('idx_hospital_type_status', 'hospital_type', 'status'),
        {'comment': 'Main hospital entity with infrastructure details'}
    )
    
    # Validators
    @validates('email')
    def validate_email(self, key, value):
        """Validate email format"""
        if value and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise ValueError("Invalid email format")
        return value
    
    @validates('hospital_type')
    def validate_hospital_type(self, key, value):
        """Validate hospital type"""
        valid_types = [
            'general', 'specialized', 'clinic', 'multi_specialty',
            'teaching', 'trauma_center', 'maternity', 'pediatric'
        ]
        if value.lower() not in valid_types:
            raise ValueError(f"Hospital type must be one of: {', '.join(valid_types)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        """Validate status"""
        valid_statuses = ['active', 'inactive', 'under_construction', 'temporary_closed']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    # Properties
    @property
    def total_floor_count(self) -> int:
        """Total floors including basement"""
        return self.total_floors + self.basement_floors
    
    @property
    def floor_range(self) -> tuple:
        """Return floor range (min, max)"""
        return (-self.basement_floors, self.total_floors)
    
    @property
    def full_address(self) -> str:
        """Return complete address"""
        return f"{self.address}, {self.city}, {self.state} {self.pincode}, {self.country}"
    
    def __repr__(self) -> str:
        """String representation"""
        return f"<Hospital(id={self.id}, name='{self.name}', code='{self.code}', floors={self.total_floors})>"
    
