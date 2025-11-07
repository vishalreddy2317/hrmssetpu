"""
Payment Model
Payment transactions and receipts
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional
from decimal import Decimal

from .base import BaseModel


class Payment(BaseModel):
    """
    Payment transaction model
    """
    
    __tablename__ = "payments"
    
    # Payment Details
    payment_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    receipt_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    payment_date: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    payment_time: Mapped[str] = mapped_column(String(10), nullable=False)
    
    # Billing Reference
    billing_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("billings.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Patient
    patient_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Payment Amount
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    
    # Payment Method
    payment_method: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        comment="cash, card, upi, net_banking, cheque, insurance, wallet"
    )
    
    # Payment Details (based on method)
    transaction_id: Mapped[Optional[str]] = mapped_column(String(100), unique=True, index=True)
    card_number: Mapped[Optional[str]] = mapped_column(String(20), comment="Last 4 digits")
    card_type: Mapped[Optional[str]] = mapped_column(String(20), comment="visa, mastercard, amex")
    cheque_number: Mapped[Optional[str]] = mapped_column(String(50))
    cheque_date: Mapped[Optional[str]] = mapped_column(String(20))
    bank_name: Mapped[Optional[str]] = mapped_column(String(200))
    upi_id: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='completed',
        nullable=False,
        index=True,
        comment="completed, pending, failed, refunded, cancelled"
    )
    
    # Refund Details
    is_refunded: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    refund_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2))
    refund_date: Mapped[Optional[str]] = mapped_column(String(20))
    refund_reason: Mapped[Optional[str]] = mapped_column(Text)
    
    # Received By
    received_by: Mapped[str] = mapped_column(String(200), nullable=False)
    
    # Notes
    payment_notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Receipt
    receipt_url: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Relationships
    billing: Mapped["Billing"] = relationship(
        "Billing",
        back_populates="payments"
    )
    
    patient: Mapped["Patient"] = relationship(
        "Patient",
        backref="payments"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('amount > 0', name='payment_positive_amount'),
        CheckConstraint('refund_amount >= 0 OR refund_amount IS NULL', name='payment_positive_refund'),
        Index('idx_payment_billing', 'billing_id', 'payment_date'),
        Index('idx_payment_patient', 'patient_id', 'payment_date'),
        Index('idx_payment_method', 'payment_method', 'status'),
        Index('idx_payment_date_status', 'payment_date', 'status'),
        {'comment': 'Payment transactions and receipts'}
    )
    
    # Validators
    @validates('payment_method')
    def validate_payment_method(self, key, value):
        valid_methods = [
            'cash', 'card', 'credit_card', 'debit_card', 'upi',
            'net_banking', 'cheque', 'insurance', 'wallet', 'online'
        ]
        if value.lower() not in valid_methods:
            raise ValueError(f"Payment method must be one of: {', '.join(valid_methods)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['completed', 'pending', 'failed', 'refunded', 'cancelled', 'processing']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<Payment(id={self.id}, number='{self.payment_number}', amount={self.amount}, method='{self.payment_method}')>"