"""
Transport Model
Ambulance and patient transport management
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional
from decimal import Decimal

from .base import BaseModel


class Transport(BaseModel):
    """
    Transport and ambulance service model
    """
    
    __tablename__ = "transports"
    
    # Transport Details
    transport_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    
    # Ambulance Reference
    ambulance_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("ambulances.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Patient (if applicable)
    patient_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("patients.id", ondelete="SET NULL"),
        index=True
    )
    
    # Transport Type
    transport_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        comment="emergency, scheduled, inter_facility, discharge, admission"
    )
    
    # Locations
    from_location: Mapped[str] = mapped_column(String(200), nullable=False)
    to_location: Mapped[str] = mapped_column(String(200), nullable=False)
    
    from_address: Mapped[Optional[str]] = mapped_column(Text)
    to_address: Mapped[Optional[str]] = mapped_column(Text)
    
    # Distance
    distance_km: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    
    # Request Details
    request_date: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    request_time: Mapped[str] = mapped_column(String(10), nullable=False)
    requested_by: Mapped[str] = mapped_column(String(200), nullable=False)
    
    # Scheduled Time
    scheduled_pickup_time: Mapped[Optional[str]] = mapped_column(String(50))
    scheduled_dropoff_time: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Actual Times
    pickup_time: Mapped[Optional[str]] = mapped_column(String(50))
    dropoff_time: Mapped[Optional[str]] = mapped_column(String(50))
    
    departure_time: Mapped[Optional[str]] = mapped_column(String(50))
    arrival_time: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Duration (in minutes)
    total_duration_minutes: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Priority
    priority: Mapped[str] = mapped_column(
        String(20),
        default='normal',
        nullable=False,
        comment="emergency, urgent, normal, scheduled"
    )
    
    # Patient Condition
    patient_condition: Mapped[Optional[str]] = mapped_column(Text)
    requires_oxygen: Mapped[bool] = mapped_column(Boolean, default=False)
    requires_ventilator: Mapped[bool] = mapped_column(Boolean, default=False)
    requires_stretcher: Mapped[bool] = mapped_column(Boolean, default=True)
    is_critical: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Staff
    driver_name: Mapped[Optional[str]] = mapped_column(String(200))
    paramedic_name: Mapped[Optional[str]] = mapped_column(String(200))
    nurse_name: Mapped[Optional[str]] = mapped_column(String(200))
    doctor_name: Mapped[Optional[str]] = mapped_column(String(200))
    
    # Contact
    contact_person: Mapped[Optional[str]] = mapped_column(String(200))
    contact_phone: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Cost
    estimated_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    actual_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='requested',
        nullable=False,
        index=True,
        comment="requested, assigned, in_transit, completed, cancelled"
    )
    
    # Incident Reports
    incident_reported: Mapped[bool] = mapped_column(Boolean, default=False)
    incident_description: Mapped[Optional[str]] = mapped_column(Text)
    
    # Vital Signs During Transport
    vital_signs_recorded: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array of vital signs")
    
    # Treatment Given
    treatment_given: Mapped[Optional[str]] = mapped_column(Text)
    
    # Feedback
    service_rating: Mapped[Optional[int]] = mapped_column(Integer)
    feedback: Mapped[Optional[str]] = mapped_column(Text)
    
    # Notes
    special_instructions: Mapped[Optional[str]] = mapped_column(Text)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationships
    ambulance: Mapped["Ambulance"] = relationship(
        "Ambulance",
        back_populates="transports"
    )
    
    patient: Mapped[Optional["Patient"]] = relationship(
        "Patient",
        backref="transports"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('distance_km >= 0 OR distance_km IS NULL', name='transport_positive_distance'),
        CheckConstraint('estimated_cost >= 0 OR estimated_cost IS NULL', name='transport_positive_estimated_cost'),
        CheckConstraint('actual_cost >= 0 OR actual_cost IS NULL', name='transport_positive_actual_cost'),
        CheckConstraint('service_rating >= 1 AND service_rating <= 5 OR service_rating IS NULL', name='transport_valid_rating'),
        Index('idx_transport_ambulance', 'ambulance_id', 'request_date'),
        Index('idx_transport_patient', 'patient_id', 'request_date'),
        Index('idx_transport_type', 'transport_type', 'status'),
        Index('idx_transport_priority', 'priority', 'status'),
        {'comment': 'Ambulance and patient transport management'}
    )
    
    # Validators
    @validates('transport_type')
    def validate_transport_type(cls, v):
        valid = ['emergency', 'scheduled', 'inter_facility', 'discharge', 'admission', 'transfer']
        if v.lower() not in valid:
            raise ValueError(f"Transport type must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validates('priority')
    def validate_priority(cls, v):
        valid = ['emergency', 'urgent', 'normal', 'scheduled']
        if v.lower() not in valid:
            raise ValueError(f"Priority must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validates('status')
    def validate_status(cls, v):
        valid = ['requested', 'assigned', 'dispatched', 'in_transit', 'completed', 'cancelled']
        if v.lower() not in valid:
            raise ValueError(f"Status must be one of: {', '.join(valid)}")
        return v.lower()
    
    def __repr__(self) -> str:
        return f"<Transport(id={self.id}, number='{self.transport_number}', type='{self.transport_type}')>"