"""
Inventory Model
General inventory and supplies management
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional
from decimal import Decimal

from .base import BaseModel


class Inventory(BaseModel):
    """
    General inventory and supplies model
    """
    
    __tablename__ = "inventories"
    
    # Item Details
    item_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    item_name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    
    # Category
    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        comment="medical_supplies, surgical_supplies, consumables, stationery, cleaning, food"
    )
    subcategory: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Description
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    # Unit
    unit_of_measurement: Mapped[str] = mapped_column(String(20), nullable=False, comment="pieces, boxes, kg, liters")
    
    # Stock Information
    current_stock: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    minimum_stock: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    maximum_stock: Mapped[int] = mapped_column(Integer, default=1000, nullable=False)
    reorder_level: Mapped[int] = mapped_column(Integer, default=20, nullable=False)
    
    # Pricing
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    total_value: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal('0.00'))
    
    # Supplier
    supplier_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("suppliers.id", ondelete="SET NULL"),
        index=True
    )
    supplier_name: Mapped[Optional[str]] = mapped_column(String(200))
    
    # Location
    storage_location: Mapped[Optional[str]] = mapped_column(String(200))
    shelf_number: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Batch/Lot
    batch_number: Mapped[Optional[str]] = mapped_column(String(50))
    manufacturing_date: Mapped[Optional[str]] = mapped_column(String(20))
    expiry_date: Mapped[Optional[str]] = mapped_column(String(20), index=True)
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='active',
        nullable=False,
        index=True,
        comment="active, discontinued, expired, out_of_stock"
    )
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Tracking
    barcode: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
    sku: Mapped[Optional[str]] = mapped_column(String(50), unique=True)
    
    # Last Restock
    last_restocked_date: Mapped[Optional[str]] = mapped_column(String(20))
    last_restocked_quantity: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Usage
    total_consumed: Mapped[int] = mapped_column(Integer, default=0)
    
    # Notes
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationships
    supplier: Mapped[Optional["Supplier"]] = relationship(
        "Supplier",
        backref="inventory_items"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('current_stock >= 0', name='inventory_positive_current_stock'),
        CheckConstraint('minimum_stock >= 0', name='inventory_positive_minimum_stock'),
        CheckConstraint('maximum_stock >= minimum_stock', name='inventory_max_greater_than_min'),
        CheckConstraint('reorder_level >= 0', name='inventory_positive_reorder_level'),
        CheckConstraint('unit_price >= 0', name='inventory_positive_unit_price'),
        CheckConstraint('total_value >= 0', name='inventory_positive_total_value'),
        Index('idx_inventory_category', 'category', 'status'),
        Index('idx_inventory_stock', 'current_stock', 'reorder_level'),
        Index('idx_inventory_expiry', 'expiry_date', 'status'),
        {'comment': 'General inventory and supplies management'}
    )
    
    # Validators
    @validates('category')
    def validate_category(self, key, value):
        valid_categories = [
            'medical_supplies', 'surgical_supplies', 'consumables',
            'stationery', 'cleaning', 'food', 'linen', 'ppe'
        ]
        if value.lower() not in valid_categories:
            raise ValueError(f"Category must be one of: {', '.join(valid_categories)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['active', 'discontinued', 'expired', 'out_of_stock', 'recalled']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    @property
    def is_low_stock(self) -> bool:
        """Check if stock is below reorder level"""
        return self.current_stock <= self.reorder_level
    
    @property
    def stock_percentage(self) -> float:
        """Calculate stock percentage"""
        if self.maximum_stock > 0:
            return (self.current_stock / self.maximum_stock) * 100
        return 0.0
    
    def __repr__(self) -> str:
        return f"<Inventory(id={self.id}, name='{self.item_name}', stock={self.current_stock})>"