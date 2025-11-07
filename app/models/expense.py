"""
Expense Model
Hospital expenses and costs tracking
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional
from decimal import Decimal

from .base import BaseModel


class Expense(BaseModel):
    """
    Expense tracking model
    """
    
    __tablename__ = "expenses"
    
    # Expense Details
    expense_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    expense_date: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    
    # Category
    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        comment="salaries, utilities, supplies, maintenance, equipment, rent, insurance, taxes"
    )
    subcategory: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Description
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Amount
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal('0.00'))
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    
    # Department (if applicable)
    department_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("departments.id", ondelete="SET NULL"),
        index=True
    )
    
    # Vendor/Supplier
    vendor_name: Mapped[Optional[str]] = mapped_column(String(200))
    vendor_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("vendors.id", ondelete="SET NULL")
    )
    
    # Invoice
    invoice_number: Mapped[Optional[str]] = mapped_column(String(50))
    invoice_date: Mapped[Optional[str]] = mapped_column(String(20))
    invoice_url: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Payment
    payment_method: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="cash, cheque, bank_transfer, card, online"
    )
    payment_status: Mapped[str] = mapped_column(
        String(20),
        default='pending',
        nullable=False,
        index=True,
        comment="pending, paid, partially_paid, overdue"
    )
    payment_date: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Approval
    approved_by: Mapped[Optional[str]] = mapped_column(String(200))
    approval_date: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Recurring
    is_recurring: Mapped[bool] = mapped_column(Boolean, default=False)
    recurrence_frequency: Mapped[Optional[str]] = mapped_column(String(20), comment="monthly, quarterly, yearly")
    
    # Notes
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationships
    department: Mapped[Optional["Department"]] = relationship(
        "Department",
        backref="expenses"
    )
    
    vendor: Mapped[Optional["Vendor"]] = relationship(
        "Vendor",
        backref="expenses"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('amount > 0', name='expense_positive_amount'),
        CheckConstraint('tax_amount >= 0', name='expense_positive_tax'),
        CheckConstraint('total_amount > 0', name='expense_positive_total'),
        Index('idx_expense_category', 'category', 'expense_date'),
        Index('idx_expense_department', 'department_id', 'expense_date'),
        Index('idx_expense_payment', 'payment_status', 'expense_date'),
        {'comment': 'Hospital expenses and costs tracking'}
    )
    
    # Validators
    @validates('category')
    def validate_category(self, key, value):
        valid_categories = [
            'salaries', 'utilities', 'supplies', 'maintenance',
            'equipment', 'rent', 'insurance', 'taxes', 'marketing',
            'administrative', 'medical_supplies', 'pharmaceuticals'
        ]
        if value.lower() not in valid_categories:
            raise ValueError(f"Category must be one of: {', '.join(valid_categories)}")
        return value.lower()
    
    @validates('payment_status')
    def validate_payment_status(self, key, value):
        valid_statuses = ['pending', 'paid', 'partially_paid', 'overdue']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Payment status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<Expense(id={self.id}, number='{self.expense_number}', amount={self.total_amount})>"