"""
Revenue Model
Hospital revenue and income tracking
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional
from decimal import Decimal

from .base import BaseModel


class Revenue(BaseModel):
    """
    Revenue tracking model
    """
    
    __tablename__ = "revenues"
    
    # Revenue Details
    revenue_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    revenue_date: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    
    # Source
    revenue_source: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        comment="consultations, procedures, pharmacy, lab, imaging, room_charges, miscellaneous"
    )
    
    # Description
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Amount
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal('0.00'))
    discount_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal('0.00'))
    net_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    
    # Patient (if applicable)
    patient_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("patients.id", ondelete="SET NULL"),
        index=True
    )
    
    # Related Records
    billing_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("billings.id", ondelete="SET NULL")
    )
    payment_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("payments.id", ondelete="SET NULL")
    )
    
    # Department
    department_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("departments.id", ondelete="SET NULL"),
        index=True
    )
    
    # Payment Method
    payment_method: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='received',
        nullable=False,
        comment="received, pending, refunded"
    )
    
    # Notes
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationships
    patient: Mapped[Optional["Patient"]] = relationship(
        "Patient",
        backref="revenues"
    )
    
    billing: Mapped[Optional["Billing"]] = relationship(
        "Billing",
        backref="revenues"
    )
    
    payment: Mapped[Optional["Payment"]] = relationship(
        "Payment",
        backref="revenues"
    )
    
    department: Mapped[Optional["Department"]] = relationship(
        "Department",
        backref="revenues"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('amount > 0', name='revenue_positive_amount'),
        CheckConstraint('tax_amount >= 0', name='revenue_positive_tax'),
        CheckConstraint('discount_amount >= 0', name='revenue_positive_discount'),
        CheckConstraint('net_amount >= 0', name='revenue_positive_net'),
        Index('idx_revenue_source', 'revenue_source', 'revenue_date'),
        Index('idx_revenue_patient', 'patient_id', 'revenue_date'),
        Index('idx_revenue_department', 'department_id', 'revenue_date'),
        {'comment': 'Hospital revenue and income tracking'}
    )
    
    # Validators
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['received', 'pending', 'refunded', 'cancelled']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<Revenue(id={self.id}, number='{self.revenue_number}', amount={self.net_amount})>"
    