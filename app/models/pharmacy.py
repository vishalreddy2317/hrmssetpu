"""
Pharmacy Model
Pharmacy transactions and medicine dispensing
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional
from decimal import Decimal

from .base import BaseModel


class Pharmacy(BaseModel):
    """
    Pharmacy transaction model
    """
    
    __tablename__ = "pharmacies"
    
    # Transaction Details
    transaction_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    transaction_date: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    transaction_time: Mapped[str] = mapped_column(String(10), nullable=False)
    
    # Prescription Reference
    prescription_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("prescriptions.id", ondelete="SET NULL"),
        index=True
    )
    
    # Patient
    patient_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Medicine Details (JSON format for multiple medicines)
    medicines_dispensed: Mapped[str] = mapped_column(Text, nullable=False, comment="JSON array")
    
    # Dispensed By
    dispensed_by: Mapped[str] = mapped_column(String(200), nullable=False)
    pharmacist_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("staffs.id", ondelete="SET NULL")
    )
    
    # Financial
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    discount_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal('0.00'))
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal('0.00'))
    final_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    
    # Payment
    payment_status: Mapped[str] = mapped_column(
        String(20),
        default='pending',
        nullable=False,
        index=True,
        comment="pending, paid, partially_paid, insurance_claimed"
    )
    payment_method: Mapped[Optional[str]] = mapped_column(
        String(50),
        comment="cash, card, insurance, online"
    )
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='completed',
        nullable=False,
        index=True,
        comment="completed, cancelled, returned, partially_returned"
    )
    
    # Return/Refund
    is_returned: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    return_date: Mapped[Optional[str]] = mapped_column(String(20))
    return_reason: Mapped[Optional[str]] = mapped_column(Text)
    refund_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    
    # Notes
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationships
    prescription: Mapped[Optional["Prescription"]] = relationship(
        "Prescription",
        backref="pharmacy_transactions"
    )
    
    patient: Mapped["Patient"] = relationship(
        "Patient",
        backref="pharmacy_transactions"
    )
    
    pharmacist: Mapped[Optional["Staff"]] = relationship(
        "Staff",
        backref="pharmacy_transactions"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('total_amount >= 0', name='pharmacy_positive_total'),
        CheckConstraint('discount_amount >= 0', name='pharmacy_positive_discount'),
        CheckConstraint('final_amount >= 0', name='pharmacy_positive_final'),
        Index('idx_pharmacy_patient', 'patient_id', 'transaction_date'),
        Index('idx_pharmacy_prescription', 'prescription_id'),
        Index('idx_pharmacy_payment', 'payment_status', 'status'),
        {'comment': 'Pharmacy transactions and medicine dispensing'}
    )
    
    # Validators
    @validates('payment_status')
    def validate_payment_status(self, key, value):
        valid_statuses = ['pending', 'paid', 'partially_paid', 'insurance_claimed', 'refunded']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Payment status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['completed', 'cancelled', 'returned', 'partially_returned']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<Pharmacy(id={self.id}, number='{self.transaction_number}', amount={self.final_amount})>"