"""
Ambulance Model
Ambulance fleet and service management
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional, List
from decimal import Decimal

from .base import BaseModel


class Ambulance(BaseModel):
    """
    Ambulance vehicle and service model
    """
    
    __tablename__ = "ambulances"
    
    # Vehicle Details
    ambulance_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    vehicle_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    vehicle_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="basic, advanced, air, mobile_icu, patient_transport"
    )
    
    # Vehicle Information
    manufacturer: Mapped[Optional[str]] = mapped_column(String(100))
    model: Mapped[Optional[str]] = mapped_column(String(100))
    year: Mapped[Optional[int]] = mapped_column(Integer)
    color: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Hospital
    hospital_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("hospitals.id", ondelete="SET NULL"),
        index=True
    )
    
    # Driver Details
    driver_name: Mapped[Optional[str]] = mapped_column(String(200))
    driver_phone: Mapped[Optional[str]] = mapped_column(String(20))
    driver_license: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Equipment
    has_oxygen: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    has_ventilator: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_defibrillator: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_ecg: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_stretcher: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    has_wheelchair: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Capacity
    patient_capacity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    staff_capacity: Mapped[int] = mapped_column(Integer, default=2, nullable=False)
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='available',
        nullable=False,
        index=True,
        comment="available, on_duty, maintenance, out_of_service"
    )
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    
    # Current Location (for tracking)
    current_latitude: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 8))
    current_longitude: Mapped[Optional[Decimal]] = mapped_column(Numeric(11, 8))
    current_location: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Maintenance
    last_maintenance_date: Mapped[Optional[str]] = mapped_column(String(20))
    next_maintenance_date: Mapped[Optional[str]] = mapped_column(String(20))
    mileage: Mapped[Optional[int]] = mapped_column(Integer, comment="in kilometers")
    
    # Insurance
    insurance_number: Mapped[Optional[str]] = mapped_column(String(100))
    insurance_expiry: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Registration
    registration_number: Mapped[Optional[str]] = mapped_column(String(50))
    registration_expiry: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Cost
    fuel_type: Mapped[Optional[str]] = mapped_column(String(20), comment="petrol, diesel, cng, electric")
    base_charge: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    per_km_charge: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    
    # Notes
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationships
    hospital: Mapped[Optional["Hospital"]] = relationship(
        "Hospital",
        backref="ambulances"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('patient_capacity > 0', name='ambulance_positive_patient_capacity'),
        CheckConstraint('staff_capacity >= 0', name='ambulance_positive_staff_capacity'),
        CheckConstraint('mileage >= 0 OR mileage IS NULL', name='ambulance_positive_mileage'),
        CheckConstraint('base_charge >= 0 OR base_charge IS NULL', name='ambulance_positive_base_charge'),
        CheckConstraint('per_km_charge >= 0 OR per_km_charge IS NULL', name='ambulance_positive_per_km_charge'),
        Index('idx_ambulance_hospital', 'hospital_id', 'status'),
        Index('idx_ambulance_availability', 'is_available', 'status'),
        {'comment': 'Ambulance fleet and service management'}
    )
    
    # Validators
    @validates('vehicle_type')
    def validate_vehicle_type(self, key, value):
        valid_types = ['basic', 'advanced', 'air', 'mobile_icu', 'patient_transport', 'neonatal']
        if value.lower() not in valid_types:
            raise ValueError(f"Vehicle type must be one of: {', '.join(valid_types)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['available', 'on_duty', 'maintenance', 'out_of_service', 'retired']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<Ambulance(id={self.id}, number='{self.ambulance_number}', vehicle='{self.vehicle_number}', status='{self.status}')>"