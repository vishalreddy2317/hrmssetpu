"""
Payroll Schemas
"""

from pydantic import BaseModel, Field, validator, condecimal
from typing import Optional
from datetime import datetime
from decimal import Decimal


# Base Schema
class PayrollBase(BaseModel):
    payroll_number: str = Field(..., max_length=20, description="Unique payroll number")
    month: int = Field(..., ge=1, le=12, description="Month (1-12)")
    year: int = Field(..., ge=2000, le=2100)
    employee_name: str = Field(..., max_length=200)
    employee_id: str = Field(..., max_length=50)


# Create Schema
class PayrollCreate(PayrollBase):
    pay_period_start: str = Field(..., max_length=20)
    pay_period_end: str = Field(..., max_length=20)
    
    staff_id: Optional[int] = None
    doctor_id: Optional[int] = None
    nurse_id: Optional[int] = None
    
    designation: Optional[str] = Field(None, max_length=100)
    
    # Salary Components
    basic_salary: condecimal(max_digits=12, decimal_places=2, ge=0) = Field(...)
    hra: condecimal(max_digits=12, decimal_places=2, ge=0) = Field(default=Decimal('0.00'))
    medical_allowance: condecimal(max_digits=12, decimal_places=2, ge=0) = Field(default=Decimal('0.00'))
    transport_allowance: condecimal(max_digits=12, decimal_places=2, ge=0) = Field(default=Decimal('0.00'))
    other_allowances: condecimal(max_digits=12, decimal_places=2, ge=0) = Field(default=Decimal('0.00'))
    
    # Overtime
    overtime_hours: int = Field(default=0, ge=0)
    overtime_amount: condecimal(max_digits=10, decimal_places=2, ge=0) = Field(default=Decimal('0.00'))
    
    # Bonuses
    bonus: condecimal(max_digits=10, decimal_places=2, ge=0) = Field(default=Decimal('0.00'))
    incentives: condecimal(max_digits=10, decimal_places=2, ge=0) = Field(default=Decimal('0.00'))
    
    # Gross Salary
    gross_salary: condecimal(max_digits=12, decimal_places=2, ge=0) = Field(...)
    
    # Deductions
    pf_deduction: condecimal(max_digits=10, decimal_places=2, ge=0) = Field(default=Decimal('0.00'))
    esi_deduction: condecimal(max_digits=10, decimal_places=2, ge=0) = Field(default=Decimal('0.00'))
    tax_deduction: condecimal(max_digits=10, decimal_places=2, ge=0) = Field(default=Decimal('0.00'))
    loan_deduction: condecimal(max_digits=10, decimal_places=2, ge=0) = Field(default=Decimal('0.00'))
    advance_deduction: condecimal(max_digits=10, decimal_places=2, ge=0) = Field(default=Decimal('0.00'))
    other_deductions: condecimal(max_digits=10, decimal_places=2, ge=0) = Field(default=Decimal('0.00'))
    
    total_deductions: condecimal(max_digits=12, decimal_places=2, ge=0) = Field(default=Decimal('0.00'))
    
    # Net Salary
    net_salary: condecimal(max_digits=12, decimal_places=2, ge=0) = Field(...)
    
    # Attendance
    working_days: int = Field(..., gt=0)
    present_days: int = Field(..., ge=0)
    absent_days: int = Field(default=0, ge=0)
    leave_days: int = Field(default=0, ge=0)
    paid_leaves: int = Field(default=0, ge=0)
    unpaid_leaves: int = Field(default=0, ge=0)
    
    # Payment
    payment_date: Optional[str] = Field(None, max_length=20)
    payment_method: Optional[str] = Field(None, max_length=50)
    transaction_id: Optional[str] = Field(None, max_length=100)
    
    status: str = Field(default='pending', max_length=20)
    
    # Bank Details
    bank_name: Optional[str] = Field(None, max_length=200)
    account_number: Optional[str] = Field(None, max_length=50)
    
    # Approval
    approved_by: Optional[str] = Field(None, max_length=200)
    approval_date: Optional[str] = Field(None, max_length=20)
    
    payslip_url: Optional[str] = Field(None, max_length=500)
    notes: Optional[str] = None
    
    @validator('status')
    def validate_status(cls, v):
        valid = ['pending', 'processed', 'paid', 'on_hold', 'cancelled']
        if v.lower() not in valid:
            raise ValueError(f"Status must be one of: {', '.join(valid)}")
        return v.lower()


# Update Schema
class PayrollUpdate(BaseModel):
    designation: Optional[str] = Field(None, max_length=100)
    
    basic_salary: Optional[condecimal(max_digits=12, decimal_places=2, ge=0)] = None
    hra: Optional[condecimal(max_digits=12, decimal_places=2, ge=0)] = None
    medical_allowance: Optional[condecimal(max_digits=12, decimal_places=2, ge=0)] = None
    transport_allowance: Optional[condecimal(max_digits=12, decimal_places=2, ge=0)] = None
    other_allowances: Optional[condecimal(max_digits=12, decimal_places=2, ge=0)] = None
    
    overtime_hours: Optional[int] = Field(None, ge=0)
    overtime_amount: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    
    bonus: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    incentives: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    
    gross_salary: Optional[condecimal(max_digits=12, decimal_places=2, ge=0)] = None
    
    pf_deduction: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    esi_deduction: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    tax_deduction: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    loan_deduction: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    advance_deduction: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    other_deductions: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    total_deductions: Optional[condecimal(max_digits=12, decimal_places=2, ge=0)] = None
    
    net_salary: Optional[condecimal(max_digits=12, decimal_places=2, ge=0)] = None
    
    present_days: Optional[int] = Field(None, ge=0)
    absent_days: Optional[int] = Field(None, ge=0)
    leave_days: Optional[int] = Field(None, ge=0)
    paid_leaves: Optional[int] = Field(None, ge=0)
    unpaid_leaves: Optional[int] = Field(None, ge=0)
    
    payment_date: Optional[str] = Field(None, max_length=20)
    payment_method: Optional[str] = Field(None, max_length=50)
    transaction_id: Optional[str] = Field(None, max_length=100)
    
    status: Optional[str] = Field(None, max_length=20)
    
    bank_name: Optional[str] = Field(None, max_length=200)
    account_number: Optional[str] = Field(None, max_length=50)
    
    approved_by: Optional[str] = Field(None, max_length=200)
    approval_date: Optional[str] = Field(None, max_length=20)
    
    payslip_url: Optional[str] = Field(None, max_length=500)
    notes: Optional[str] = None


# Response Schema
class PayrollResponse(PayrollBase):
    id: int
    pay_period_start: str
    pay_period_end: str
    
    staff_id: Optional[int]
    doctor_id: Optional[int]
    nurse_id: Optional[int]
    
    designation: Optional[str]
    
    basic_salary: Decimal
    hra: Decimal
    medical_allowance: Decimal
    transport_allowance: Decimal
    other_allowances: Decimal
    
    overtime_hours: int
    overtime_amount: Decimal
    
    bonus: Decimal
    incentives: Decimal
    
    gross_salary: Decimal
    
    pf_deduction: Decimal
    esi_deduction: Decimal
    tax_deduction: Decimal
    loan_deduction: Decimal
    advance_deduction: Decimal
    other_deductions: Decimal
    total_deductions: Decimal
    
    net_salary: Decimal
    
    working_days: int
    present_days: int
    absent_days: int
    leave_days: int
    paid_leaves: int
    unpaid_leaves: int
    
    payment_date: Optional[str]
    payment_method: Optional[str]
    transaction_id: Optional[str]
    
    status: str
    
    bank_name: Optional[str]
    account_number: Optional[str]
    
    approved_by: Optional[str]
    approval_date: Optional[str]
    
    payslip_url: Optional[str]
    notes: Optional[str]
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v)
        }


# List Response
class PayrollListResponse(BaseModel):
    total: int
    items: list[PayrollResponse]
    page: int
    page_size: int
    total_pages: int


# Approve Payroll Schema
class PayrollApproveSchema(BaseModel):
    approved_by: str = Field(..., max_length=200)
    approval_date: str = Field(..., max_length=20)


# Process Payment Schema
class PayrollProcessPaymentSchema(BaseModel):
    payment_date: str = Field(..., max_length=20)
    payment_method: str = Field(..., max_length=50)
    transaction_id: str = Field(..., max_length=100)