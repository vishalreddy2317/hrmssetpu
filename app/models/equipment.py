"""
Equipment Model
Medical equipment and asset tracking with floor location
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint, Numeric, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional
from decimal import Decimal

from .base import BaseModel


class Equipment(BaseModel):
    """
    Medical equipment and assets model with floor tracking
    """
    
    __tablename__ = "equipments"
    
    # Equipment Details
    equipment_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    equipment_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        comment="diagnostic, surgical, monitoring, life_support, imaging, laboratory"
    )
    
    # Category
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    subcategory: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Manufacturer Details
    manufacturer: Mapped[str] = mapped_column(String(200), nullable=False)
    model_number: Mapped[str] = mapped_column(String(100), nullable=False)
    serial_number: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    
    # Purchase Details
    purchase_date: Mapped[Optional[str]] = mapped_column(String(20))
    purchase_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2))
    supplier: Mapped[Optional[str]] = mapped_column(String(200))
    warranty_expiry_date: Mapped[Optional[str]] = mapped_column(String(20))
    
    # ⭐ Location - Floor Reference
    floor_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("floors.id", ondelete="SET NULL"),
        index=True
    )
    floor_number: Mapped[Optional[int]] = mapped_column(Integer, index=True)
    department_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("departments.id", ondelete="SET NULL"),
        index=True
    )
    room_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("rooms.id", ondelete="SET NULL")
    )
    current_location: Mapped[Optional[str]] = mapped_column(String(200))
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='available',
        nullable=False,
        index=True,
        comment="available, in_use, maintenance, repair, out_of_service, disposed"
    )
    is_operational: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Condition
    condition: Mapped[str] = mapped_column(
        String(20),
        default='good',
        nullable=False,
        comment="excellent, good, fair, poor, critical"
    )
    
    # Maintenance
    last_maintenance_date: Mapped[Optional[str]] = mapped_column(String(20))
    next_maintenance_date: Mapped[Optional[str]] = mapped_column(String(20), index=True)
    maintenance_frequency_days: Mapped[Optional[int]] = mapped_column(Integer)
    maintenance_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    
    # Calibration (for precision equipment)
    requires_calibration: Mapped[bool] = mapped_column(Boolean, default=False)
    last_calibration_date: Mapped[Optional[str]] = mapped_column(String(20))
    next_calibration_date: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Safety & Compliance
    requires_certification: Mapped[bool] = mapped_column(Boolean, default=False)
    certification_number: Mapped[Optional[str]] = mapped_column(String(100))
    certification_expiry: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Assignment
    assigned_to: Mapped[Optional[str]] = mapped_column(String(200))
    assigned_to_staff_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("staffs.id", ondelete="SET NULL")
    )
    
    # Usage
    is_portable: Mapped[bool] = mapped_column(Boolean, default=False)
    requires_training: Mapped[bool] = mapped_column(Boolean, default=False)
    usage_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Specifications
    specifications: Mapped[Optional[str]] = mapped_column(Text, comment="JSON format")
    operating_instructions: Mapped[Optional[str]] = mapped_column(Text)
    
    # Documents
    manual_url: Mapped[Optional[str]] = mapped_column(String(500))
    certificate_url: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Asset Management
    asset_tag: Mapped[Optional[str]] = mapped_column(String(50), unique=True)
    barcode: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
    qr_code: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Depreciation
    depreciation_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2))
    current_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2))
    
    # Notes
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationships
    floor: Mapped[Optional["Floor"]] = relationship(
        "Floor",
        back_populates="equipment"
    )
    
    department: Mapped[Optional["Department"]] = relationship(
        "Department",
        backref="equipment_list"
    )
    
    room: Mapped[Optional["Room"]] = relationship(
        "Room",
        backref="equipment_list"
    )
    
    assigned_staff: Mapped[Optional["Staff"]] = relationship(
        "Staff",
        backref="assigned_equipment"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('purchase_price >= 0 OR purchase_price IS NULL', name='equipment_positive_purchase_price'),
        CheckConstraint('maintenance_cost >= 0 OR maintenance_cost IS NULL', name='equipment_positive_maintenance_cost'),
        CheckConstraint('usage_count >= 0', name='equipment_positive_usage_count'),
        CheckConstraint('depreciation_rate >= 0 AND depreciation_rate <= 100 OR depreciation_rate IS NULL', name='equipment_valid_depreciation_rate'),
        Index('idx_equipment_floor', 'floor_id', 'status'),
        Index('idx_equipment_department', 'department_id', 'status'),
        Index('idx_equipment_type', 'equipment_type', 'status'),
        Index('idx_equipment_maintenance', 'next_maintenance_date', 'status'),
        {'comment': 'Medical equipment and asset tracking with floor locations'}
    )
    
    # Validators
    @validates('equipment_type')
    def validate_equipment_type(self, key, value):
        valid_types = [
            'diagnostic', 'surgical', 'monitoring', 'life_support',
            'imaging', 'laboratory', 'therapeutic', 'sterilization'
        ]
        if value.lower() not in valid_types:
            raise ValueError(f"Equipment type must be one of: {', '.join(valid_types)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['available', 'in_use', 'maintenance', 'repair', 'out_of_service', 'disposed', 'reserved']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    @validates('condition')
    def validate_condition(self, key, value):
        valid_conditions = ['excellent', 'good', 'fair', 'poor', 'critical']
        if value.lower() not in valid_conditions:
            raise ValueError(f"Condition must be one of: {', '.join(valid_conditions)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<Equipment(id={self.id}, name='{self.name}', serial='{self.serial_number}', status='{self.status}')>"