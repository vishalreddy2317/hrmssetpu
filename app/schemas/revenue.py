"""
Revenue Schemas
"""

from pydantic import BaseModel, Field, validator, condecimal
from typing import Optional
from datetime import datetime
from decimal import Decimal


# Base Schema
class RevenueBase(BaseModel):
    revenue_number: str = Field(..., max_length=20, description="Unique revenue number")
    revenue_date: str = Field(..., max_length=20)
    revenue_source: str = Field(..., max_length=100)
    description: str = Field(..., description="Revenue description")
    
    @validator('revenue_source')
    def validate_revenue_source(cls, v):
        valid = ['consultations', 'procedures', 'pharmacy', 'lab', 'imaging', 
                'room_charges', 'emergency', 'surgery', 'miscellaneous', 'insurance']
        if v.lower() not in valid:
            raise ValueError(f"Revenue source must be one of: {', '.join(valid)}")
        return v.lower()


# Create Schema
class RevenueCreate(RevenueBase):
    amount: condecimal(max_digits=12, decimal_places=2, gt=0) = Field(...)
    tax_amount: condecimal(max_digits=10, decimal_places=2, ge=0) = Field(default=Decimal('0.00'))
    discount_amount: condecimal(max_digits=10, decimal_places=2, ge=0) = Field(default=Decimal('0.00'))
    net_amount: condecimal(max_digits=12, decimal_places=2, ge=0) = Field(...)
    
    patient_id: Optional[int] = None
    billing_id: Optional[int] = None
    payment_id: Optional[int] = None
    department_id: Optional[int] = None
    
    payment_method: str = Field(..., max_length=50)
    status: str = Field(default='received', max_length=20)
    notes: Optional[str] = None
    
    @validator('status')
    def validate_status(cls, v):
        valid = ['received', 'pending', 'refunded', 'cancelled']
        if v.lower() not in valid:
            raise ValueError(f"Status must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validator('payment_method')
    def validate_payment_method(cls, v):
        valid = ['cash', 'card', 'credit_card', 'debit_card', 'upi', 'net_banking', 
                'cheque', 'insurance', 'online', 'mobile_payment']
        if v.lower() not in valid:
            raise ValueError(f"Payment method must be one of: {', '.join(valid)}")
        return v.lower()


# Update Schema
class RevenueUpdate(BaseModel):
    revenue_date: Optional[str] = Field(None, max_length=20)
    revenue_source: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    
    amount: Optional[condecimal(max_digits=12, decimal_places=2, gt=0)] = None
    tax_amount: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    discount_amount: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    net_amount: Optional[condecimal(max_digits=12, decimal_places=2, ge=0)] = None
    
    patient_id: Optional[int] = None
    billing_id: Optional[int] = None
    payment_id: Optional[int] = None
    department_id: Optional[int] = None
    
    payment_method: Optional[str] = Field(None, max_length=50)
    status: Optional[str] = Field(None, max_length=20)
    notes: Optional[str] = None


# Response Schema
class RevenueResponse(RevenueBase):
    id: int
    amount: Decimal
    tax_amount: Decimal
    discount_amount: Decimal
    net_amount: Decimal
    
    patient_id: Optional[int]
    billing_id: Optional[int]
    payment_id: Optional[int]
    department_id: Optional[int]
    
    payment_method: str
    status: str
    notes: Optional[str]
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v)
        }


# List Response
class RevenueListResponse(BaseModel):
    total: int
    total_revenue: Decimal
    items: list[RevenueResponse]
    page: int
    page_size: int
    total_pages: int
    
    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }


# Revenue Summary Schema
class RevenueSummarySchema(BaseModel):
    total_revenue: Decimal
    total_tax: Decimal
    total_discount: Decimal
    net_revenue: Decimal
    revenue_by_source: dict  # {source: amount}
    revenue_by_payment_method: dict  # {method: amount}
    revenue_count: int
    
    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }


# Revenue Filter Schema
class RevenueFilterSchema(BaseModel):
    start_date: Optional[str] = Field(None, max_length=20)
    end_date: Optional[str] = Field(None, max_length=20)
    revenue_source: Optional[str] = Field(None, max_length=100)
    department_id: Optional[int] = None
    patient_id: Optional[int] = None
    payment_method: Optional[str] = Field(None, max_length=50)
    status: Optional[str] = Field(None, max_length=20)
    min_amount: Optional[Decimal] = None
    max_amount: Optional[Decimal] = None


# Refund Revenue Schema
class RevenueRefundSchema(BaseModel):
    refund_amount: condecimal(max_digits=12, decimal_places=2, gt=0) = Field(...)
    refund_reason: str = Field(..., description="Reason for refund")
    refund_method: str = Field(..., max_length=50)
    refunded_by: str = Field(..., max_length=200)
    notes: Optional[str] = None


# Revenue by Period Schema
class RevenueByPeriodSchema(BaseModel):
    period: str = Field(..., description="daily, weekly, monthly, yearly")
    start_date: str = Field(..., max_length=20)
    end_date: str = Field(..., max_length=20)
    
    @validator('period')
    def validate_period(cls, v):
        valid = ['daily', 'weekly', 'monthly', 'quarterly', 'yearly']
        if v.lower() not in valid:
            raise ValueError(f"Period must be one of: {', '.join(valid)}")
        return v.lower()


# Revenue Report Schema
class RevenueReportSchema(BaseModel):
    report_date: str
    total_revenue: Decimal
    total_tax: Decimal
    total_discount: Decimal
    net_revenue: Decimal
    transaction_count: int
    
    # Breakdown by source
    consultations: Decimal = Decimal('0.00')
    procedures: Decimal = Decimal('0.00')
    pharmacy: Decimal = Decimal('0.00')
    lab: Decimal = Decimal('0.00')
    imaging: Decimal = Decimal('0.00')
    room_charges: Decimal = Decimal('0.00')
    miscellaneous: Decimal = Decimal('0.00')
    
    # Breakdown by payment method
    cash: Decimal = Decimal('0.00')
    card: Decimal = Decimal('0.00')
    insurance: Decimal = Decimal('0.00')
    online: Decimal = Decimal('0.00')
    other: Decimal = Decimal('0.00')
    
    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }