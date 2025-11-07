"""
Medicine Model
Medicine inventory and catalog
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, Index, CheckConstraint, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional, List
from decimal import Decimal

from .base import BaseModel


class Medicine(BaseModel):
    """
    Medicine catalog and inventory model
    """
    
    __tablename__ = "medicines"
    
    # Medicine Details
    medicine_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    generic_name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    brand_name: Mapped[Optional[str]] = mapped_column(String(200))
    
    # Classification
    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        comment="antibiotic, analgesic, antipyretic, antiviral, etc."
    )
    drug_class: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Form and Strength
    dosage_form: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="tablet, capsule, syrup, injection, ointment, drops"
    )
    strength: Mapped[str] = mapped_column(String(50), nullable=False)
    unit: Mapped[str] = mapped_column(String(20), nullable=False, comment="mg, ml, g, IU")
    
    # Manufacturer
    manufacturer: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    supplier: Mapped[Optional[str]] = mapped_column(String(200))
    
    # Stock Information
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    reorder_level: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    unit_of_measurement: Mapped[str] = mapped_column(String(20), default='units', nullable=False)
    
    # Pricing
    purchase_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    selling_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    mrp: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), comment="Maximum Retail Price")
    
    # Batch Information
    batch_number: Mapped[Optional[str]] = mapped_column(String(50))
    manufacturing_date: Mapped[Optional[str]] = mapped_column(String(20))
    expiry_date: Mapped[Optional[str]] = mapped_column(String(20), index=True)
    
    # Prescription
    requires_prescription: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_controlled_substance: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    schedule_category: Mapped[Optional[str]] = mapped_column(String(20), comment="Schedule H, X, etc.")
    
    # Usage Instructions
    usage_instructions: Mapped[Optional[str]] = mapped_column(Text)
    dosage_instructions: Mapped[Optional[str]] = mapped_column(Text)
    side_effects: Mapped[Optional[str]] = mapped_column(Text)
    contraindications: Mapped[Optional[str]] = mapped_column(Text)
    warnings: Mapped[Optional[str]] = mapped_column(Text)
    
    # Storage
    storage_conditions: Mapped[Optional[str]] = mapped_column(String(200))
    storage_location: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='active',
        nullable=False,
        index=True,
        comment="active, discontinued, out_of_stock, expired"
    )
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    
    # Additional Info
    description: Mapped[Optional[str]] = mapped_column(Text)
    barcode: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
    
    # Relationships
    prescriptions: Mapped[List["Prescription"]] = relationship(
        "Prescription",
        back_populates="medicine",
        secondary="prescription_medicines",
        lazy="dynamic"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('stock_quantity >= 0', name='medicine_positive_stock'),
        CheckConstraint('reorder_level >= 0', name='medicine_positive_reorder'),
        CheckConstraint('purchase_price > 0', name='medicine_positive_purchase_price'),
        CheckConstraint('selling_price > 0', name='medicine_positive_selling_price'),
        Index('idx_medicine_stock', 'stock_quantity', 'reorder_level'),
        Index('idx_medicine_category', 'category', 'status'),
        Index('idx_medicine_expiry', 'expiry_date', 'status'),
        {'comment': 'Medicine catalog and inventory management'}
    )
    
    # Validators
    @validates('dosage_form')
    def validate_dosage_form(self, key, value):
        valid_forms = [
            'tablet', 'capsule', 'syrup', 'injection', 'ointment',
            'cream', 'drops', 'inhaler', 'patch', 'powder', 'solution'
        ]
        if value.lower() not in valid_forms:
            raise ValueError(f"Dosage form must be one of: {', '.join(valid_forms)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['active', 'discontinued', 'out_of_stock', 'expired', 'recalled']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    @property
    def is_low_stock(self) -> bool:
        """Check if stock is below reorder level"""
        return self.stock_quantity <= self.reorder_level
    
    @property
    def profit_margin(self) -> Decimal:
        """Calculate profit margin percentage"""
        if self.purchase_price > 0:
            return ((self.selling_price - self.purchase_price) / self.purchase_price) * 100
        return Decimal(0)
    
    def __repr__(self) -> str:
        return f"<Medicine(id={self.id}, name='{self.name}', code='{self.medicine_code}', stock={self.stock_quantity})>"