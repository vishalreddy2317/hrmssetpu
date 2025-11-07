"""
Payroll Model
Staff salary and payroll management
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional
from decimal import Decimal

from .base import BaseModel


class Payroll(BaseModel):
    """
    Payroll model
    """
    
    __tablename__ = "payrolls"
    
    # Payroll Details
    payroll_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    
    # Period
    month: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    pay_period_start: Mapped[str] = mapped_column(String(20), nullable=False)
    pay_period_end: Mapped[str] = mapped_column(String(20), nullable=False)
    
    # Employee Reference
    staff_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("staffs.id", ondelete="CASCADE"),
        index=True
    )
    doctor_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("doctors.id", ondelete="CASCADE"),
        index=True
    )
    nurse_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("nurses.id", ondelete="CASCADE"),
        index=True
    )
    
    # Employee Info
    employee_name: Mapped[str] = mapped_column(String(200), nullable=False)
    employee_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    designation: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Salary Components
    basic_salary: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    hra: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal('0.00'), comment="House Rent Allowance")
    medical_allowance: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal('0.00'))
    transport_allowance: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal('0.00'))
    other_allowances: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal('0.00'))
    
    # Overtime
    overtime_hours: Mapped[int] = mapped_column(Integer, default=0)
    overtime_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal('0.00'))
    
    # Bonuses & Incentives
    bonus: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal('0.00'))
    incentives: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal('0.00'))
    
    # Gross Salary
    gross_salary: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    
    # Deductions
    pf_deduction: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal('0.00'), comment="Provident Fund")
    esi_deduction: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal('0.00'), comment="Employee State Insurance")
    tax_deduction: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal('0.00'))
    loan_deduction: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal('0.00'))
    advance_deduction: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal('0.00'))
    other_deductions: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal('0.00'))
    
    # Total Deductions
    total_deductions: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal('0.00'))
    
    # Net Salary
    net_salary: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    
    # Attendance
    working_days: Mapped[int] = mapped_column(Integer, nullable=False)
    present_days: Mapped[int] = mapped_column(Integer, nullable=False)
    absent_days: Mapped[int] = mapped_column(Integer, default=0)
    leave_days: Mapped[int] = mapped_column(Integer, default=0)
    paid_leaves: Mapped[int] = mapped_column(Integer, default=0)
    unpaid_leaves: Mapped[int] = mapped_column(Integer, default=0)
    
    # Payment
    payment_date: Mapped[Optional[str]] = mapped_column(String(20))
    payment_method: Mapped[Optional[str]] = mapped_column(String(50), comment="bank_transfer, cash, cheque")
    transaction_id: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='pending',
        nullable=False,
        index=True,
        comment="pending, processed, paid, on_hold"
    )
    
    # Bank Details (snapshot)
    bank_name: Mapped[Optional[str]] = mapped_column(String(200))
    account_number: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Approval
    approved_by: Mapped[Optional[str]] = mapped_column(String(200))
    approval_date: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Payslip
    payslip_url: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Notes
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationships
    staff: Mapped[Optional["Staff"]] = relationship(
        "Staff",
        backref="payrolls"
    )
    
    doctor: Mapped[Optional["Doctor"]] = relationship(
        "Doctor",
        backref="payrolls"
    )
    
    nurse: Mapped[Optional["Nurse"]] = relationship(
        "Nurse",
        backref="payrolls"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('month >= 1 AND month <= 12', name='payroll_valid_month'),
        CheckConstraint('year >= 2000 AND year <= 2100', name='payroll_valid_year'),
        CheckConstraint('basic_salary >= 0', name='payroll_positive_basic_salary'),
        CheckConstraint('gross_salary >= 0', name='payroll_positive_gross_salary'),
        CheckConstraint('net_salary >= 0', name='payroll_positive_net_salary'),
        CheckConstraint('working_days > 0', name='payroll_positive_working_days'),
        CheckConstraint('present_days >= 0', name='payroll_positive_present_days'),
        Index('idx_payroll_employee', 'employee_id', 'month', 'year'),
        Index('idx_payroll_period', 'month', 'year', 'status'),
        {'comment': 'Staff salary and payroll management'}
    )
    
    # Validators
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['pending', 'processed', 'paid', 'on_hold', 'cancelled']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<Payroll(id={self.id}, employee='{self.employee_name}', period={self.month}/{self.year}, net={self.net_salary})>"