"""
Stock Model
Medicine and inventory stock tracking
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional
from decimal import Decimal

from .base import BaseModel


class Stock(BaseModel):
    """
    Stock transaction and inventory tracking model
    """
    
    __tablename__ = "stocks"
    
    # Transaction Details
    transaction_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    transaction_date: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    
    # Medicine/Item Reference
    medicine_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("medicines.id", ondelete="CASCADE"),
        index=True
    )
    inventory_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("inventories.id", ondelete="CASCADE"),
        index=True
    )
    
    # Item Details
    item_name: Mapped[str] = mapped_column(String(200), nullable=False)
    item_code: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Transaction Type
    transaction_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        comment="purchase, sale, return, adjustment, transfer, damage, expiry"
    )
    
    # Quantity
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_of_measurement: Mapped[str] = mapped_column(String(20), default='units')
    
    # Previous and New Stock
    previous_stock: Mapped[int] = mapped_column(Integer, nullable=False)
    new_stock: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Pricing
    unit_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    total_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2))
    
    # Batch Information
    batch_number: Mapped[Optional[str]] = mapped_column(String(50), index=True)
    manufacturing_date: Mapped[Optional[str]] = mapped_column(String(20))
    expiry_date: Mapped[Optional[str]] = mapped_column(String(20), index=True)
    
    # Reference Documents
    purchase_order_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("purchase_orders.id", ondelete="SET NULL")
    )
    supplier_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("suppliers.id", ondelete="SET NULL")
    )
    
    # Location
    from_location: Mapped[Optional[str]] = mapped_column(String(100))
    to_location: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Personnel
    performed_by: Mapped[str] = mapped_column(String(200), nullable=False)
    approved_by: Mapped[Optional[str]] = mapped_column(String(200))
    
    # Reason
    reason: Mapped[Optional[str]] = mapped_column(Text)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='completed',
        nullable=False,
        index=True,
        comment="pending, completed, cancelled, reversed"
    )
    
    # Relationships
    medicine: Mapped[Optional["Medicine"]] = relationship(
        "Medicine",
        backref="stock_transactions"
    )
    
    inventory: Mapped[Optional["Inventory"]] = relationship(
        "Inventory",
        backref="stock_transactions"
    )
    
    supplier: Mapped[Optional["Supplier"]] = relationship(
        "Supplier",
        backref="stock_transactions"
    )
    
    purchase_order: Mapped[Optional["PurchaseOrder"]] = relationship(
        "PurchaseOrder",
        backref="stock_transactions"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('quantity != 0', name='stock_nonzero_quantity'),
        CheckConstraint('previous_stock >= 0', name='stock_positive_previous'),
        CheckConstraint('new_stock >= 0', name='stock_positive_new'),
        CheckConstraint('unit_price >= 0 OR unit_price IS NULL', name='stock_positive_price'),
        Index('idx_stock_medicine', 'medicine_id', 'transaction_date'),
        Index('idx_stock_inventory', 'inventory_id', 'transaction_date'),
        Index('idx_stock_type', 'transaction_type', 'status'),
        Index('idx_stock_batch', 'batch_number', 'expiry_date'),
        {'comment': 'Stock transactions and inventory tracking'}
    )
    
    # Validators
    @validates('transaction_type')
    def validate_transaction_type(self, key, value):
        valid_types = [
            'purchase', 'sale', 'return', 'adjustment', 'transfer',
            'damage', 'expiry', 'disposal', 'opening_stock'
        ]
        if value.lower() not in valid_types:
            raise ValueError(f"Transaction type must be one of: {', '.join(valid_types)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['pending', 'completed', 'cancelled', 'reversed']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    @property
    def quantity_change(self) -> int:
        """Get the net change in quantity"""
        return self.new_stock - self.previous_stock
    
    def __repr__(self) -> str:
        return f"<Stock(id={self.id}, number='{self.transaction_number}', type='{self.transaction_type}')>"