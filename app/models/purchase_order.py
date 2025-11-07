"""
Purchase Order Model
Purchase orders for inventory and supplies
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional
from decimal import Decimal

from .base import BaseModel


class PurchaseOrder(BaseModel):
    """
    Purchase order model
    """
    
    __tablename__ = "purchase_orders"
    
    # PO Details
    po_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    po_date: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    
    # Supplier
    supplier_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("suppliers.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Items (JSON format)
    items: Mapped[str] = mapped_column(Text, nullable=False, comment="JSON array of items")
    
    # Financial
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal('0.00'))
    shipping_cost: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal('0.00'))
    discount_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal('0.00'))
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    
    # Delivery
    expected_delivery_date: Mapped[Optional[str]] = mapped_column(String(20))
    actual_delivery_date: Mapped[Optional[str]] = mapped_column(String(20))
    delivery_address: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='pending',
        nullable=False,
        index=True,
        comment="pending, approved, rejected, ordered, partially_received, received, cancelled"
    )
    
    # Payment
    payment_status: Mapped[str] = mapped_column(
        String(20),
        default='pending',
        nullable=False,
        comment="pending, partial, paid"
    )
    payment_terms: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Approval
    requested_by: Mapped[str] = mapped_column(String(200), nullable=False)
    approved_by: Mapped[Optional[str]] = mapped_column(String(200))
    approved_date: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Notes
    notes: Mapped[Optional[str]] = mapped_column(Text)
    terms_conditions: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationships
    supplier: Mapped["Supplier"] = relationship(
        "Supplier",
        back_populates="purchase_orders"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('subtotal >= 0', name='po_positive_subtotal'),
        CheckConstraint('tax_amount >= 0', name='po_positive_tax'),
        CheckConstraint('total_amount >= 0', name='po_positive_total'),
        Index('idx_po_supplier', 'supplier_id', 'po_date'),
        Index('idx_po_status', 'status', 'payment_status'),
        {'comment': 'Purchase orders for inventory and supplies'}
    )
    
    # Validators
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = [
            'pending', 'approved', 'rejected', 'ordered',
            'partially_received', 'received', 'cancelled'
        ]
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    @validates('payment_status')
    def validate_payment_status(self, key, value):
        valid_statuses = ['pending', 'partial', 'paid']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Payment status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<PurchaseOrder(id={self.id}, number='{self.po_number}', amount={self.total_amount})>"