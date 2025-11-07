"""
Maintenance Model
Equipment maintenance logs and tracking
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional
from decimal import Decimal

from .base import BaseModel


class Maintenance(BaseModel):
    """
    Equipment maintenance log model
    """
    
    __tablename__ = "maintenance_logs"
    
    # Maintenance Details
    maintenance_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    
    # Equipment Reference
    equipment_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("equipment.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Maintenance Type
    maintenance_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        comment="preventive, corrective, emergency, calibration, inspection"
    )
    
    # Dates
    maintenance_date: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    maintenance_time: Mapped[Optional[str]] = mapped_column(String(10))
    completion_date: Mapped[Optional[str]] = mapped_column(String(20))
    completion_time: Mapped[Optional[str]] = mapped_column(String(10))
    next_maintenance_date: Mapped[Optional[str]] = mapped_column(String(20), index=True)
    
    # Problem and Action
    problem_reported: Mapped[Optional[str]] = mapped_column(Text)
    action_taken: Mapped[Optional[str]] = mapped_column(Text)
    parts_replaced: Mapped[Optional[str]] = mapped_column(Text)
    
    # Technician Details
    technician_name: Mapped[Optional[str]] = mapped_column(String(200))
    technician_contact: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Vendor Details
    vendor_name: Mapped[Optional[str]] = mapped_column(String(200))
    vendor_contact: Mapped[Optional[str]] = mapped_column(String(20))
    vendor_invoice_number: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Cost
    cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    parts_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    labor_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='pending',
        nullable=False,
        index=True,
        comment="pending, in_progress, completed, cancelled"
    )
    
    # Priority
    priority: Mapped[str] = mapped_column(
        String(20),
        default='routine',
        nullable=False,
        comment="routine, urgent, emergency"
    )
    
    # Downtime
    downtime_hours: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2))
    
    # Quality Check
    quality_check_done: Mapped[bool] = mapped_column(Boolean, default=False)
    quality_check_by: Mapped[Optional[str]] = mapped_column(String(200))
    
    # Attachments
    report_file_url: Mapped[Optional[str]] = mapped_column(String(500))
    invoice_file_url: Mapped[Optional[str]] = mapped_column(String(500))
    images_urls: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array of image URLs")
    
    # Notes
    notes: Mapped[Optional[str]] = mapped_column(Text)
    recommendations: Mapped[Optional[str]] = mapped_column(Text)
    
    # Warranty
    under_warranty: Mapped[bool] = mapped_column(Boolean, default=False)
    warranty_claim_number: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Relationships
    equipment: Mapped["Equipment"] = relationship(
        "Equipment",
        back_populates="maintenance_records"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('cost >= 0 OR cost IS NULL', name='maintenance_positive_cost'),
        CheckConstraint('parts_cost >= 0 OR parts_cost IS NULL', name='maintenance_positive_parts_cost'),
        CheckConstraint('labor_cost >= 0 OR labor_cost IS NULL', name='maintenance_positive_labor_cost'),
        CheckConstraint('downtime_hours >= 0 OR downtime_hours IS NULL', name='maintenance_positive_downtime'),
        Index('idx_maintenance_equipment', 'equipment_id', 'maintenance_date'),
        Index('idx_maintenance_type', 'maintenance_type', 'status'),
        Index('idx_maintenance_next', 'next_maintenance_date', 'status'),
        {'comment': 'Equipment maintenance logs and tracking'}
    )
    
    # Validators
    @validates('maintenance_type')
    def validate_maintenance_type(self, key, value):
        valid_types = [
            'preventive', 'corrective', 'emergency',
            'calibration', 'inspection', 'upgrade'
        ]
        if value.lower() not in valid_types:
            raise ValueError(f"Maintenance type must be one of: {', '.join(valid_types)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['pending', 'in_progress', 'completed', 'cancelled']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    @validates('priority')
    def validate_priority(self, key, value):
        valid_priorities = ['routine', 'urgent', 'emergency']
        if value.lower() not in valid_priorities:
            raise ValueError(f"Priority must be one of: {', '.join(valid_priorities)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<Maintenance(id={self.id}, number='{self.maintenance_number}', type='{self.maintenance_type}')>"