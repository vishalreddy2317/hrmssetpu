"""
Payment Schemas - Pydantic V2
Payment transaction management
"""

from typing import Optional
from pydantic import Field, field_validator, model_validator
from datetime import datetime
from decimal import Decimal

from .base import BaseSchema, BaseResponseSchema


# ============================================
# Payment Create
# ============================================

class PaymentCreate(BaseSchema):
    """Schema for creating payment"""
    
    billing_id: int = Field(..., description="Billing/Invoice ID")
    patient_id: int = Field(..., description="Patient ID")
    
    amount: Decimal = Field(..., gt=0, description="Payment amount")
    
    payment_date: str = Field(..., description="Payment date (YYYY-MM-DD)")
    payment_time: str = Field(default="00:00", description="Payment time (HH:MM)")
    
    payment_method: str = Field(
        ...,
        description="cash, card, upi, net_banking, cheque, insurance, wallet"
    )
    
    # Payment Details (based on method)
    transaction_id: Optional[str] = Field(default=None, max_length=100)
    card_number: Optional[str] = Field(default=None, max_length=20, description="Last 4 digits only")
    card_type: Optional[str] = Field(default=None, max_length=20)
    cheque_number: Optional[str] = Field(default=None, max_length=50)
    cheque_date: Optional[str] = Field(default=None, max_length=20)
    bank_name: Optional[str] = Field(default=None, max_length=200)
    upi_id: Optional[str] = Field(default=None, max_length=100)
    
    # Status
    status: str = Field(default='completed', max_length=20)
    
    # Notes
    payment_notes: Optional[str] = Field(default=None, max_length=500)
    
    # Received By
    received_by: str = Field(..., min_length=2, max_length=200)
    
    @field_validator('payment_method')
    @classmethod
    def validate_payment_method(cls, v: str) -> str:
        """Validate payment method"""
        allowed = [
            'cash', 'card', 'credit_card', 'debit_card', 'upi',
            'net_banking', 'cheque', 'insurance', 'wallet', 'online'
        ]
        if v.lower() not in allowed:
            raise ValueError(f'Payment method must be one of: {", ".join(allowed)}')
        return v.lower()
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate status"""
        allowed = ['completed', 'pending', 'failed', 'refunded', 'cancelled', 'processing']
        if v.lower() not in allowed:
            raise ValueError(f'Status must be one of: {", ".join(allowed)}')
        return v.lower()
    
    @field_validator('card_number')
    @classmethod
    def validate_card_number(cls, v: Optional[str]) -> Optional[str]:
        """Validate card number - only last 4 digits"""
        if v and len(v) > 4:
            raise ValueError("Store only last 4 digits of card number for security")
        return v


# ============================================
# Payment Update
# ============================================

class PaymentUpdate(BaseSchema):
    """Schema for updating payment"""
    
    status: Optional[str] = None
    transaction_id: Optional[str] = Field(default=None, max_length=100)
    payment_notes: Optional[str] = Field(default=None, max_length=500)


class PaymentRefund(BaseSchema):
    """Schema for payment refund"""
    
    payment_id: int
    refund_amount: Decimal = Field(..., gt=0)
    refund_reason: str = Field(..., min_length=5, max_length=500)
    refund_date: Optional[str] = Field(default=None, description="YYYY-MM-DD")


# ============================================
# Payment Response
# ============================================

class PaymentResponse(BaseResponseSchema):
    """Schema for payment response"""
    
    payment_number: str
    receipt_number: str
    payment_date: str
    payment_time: str
    
    billing_id: int
    patient_id: int
    
    amount: Decimal
    
    payment_method: str
    
    transaction_id: Optional[str] = None
    card_number: Optional[str] = None
    card_type: Optional[str] = None
    cheque_number: Optional[str] = None
    cheque_date: Optional[str] = None
    bank_name: Optional[str] = None
    upi_id: Optional[str] = None
    
    status: str
    
    is_refunded: bool = False
    refund_amount: Optional[Decimal] = None
    refund_date: Optional[str] = None
    refund_reason: Optional[str] = None
    
    received_by: str
    payment_notes: Optional[str] = None
    
    receipt_url: Optional[str] = None


class PaymentListResponse(BaseSchema):
    """Schema for payment list response"""
    
    id: int
    payment_number: str
    receipt_number: str
    payment_date: str
    patient_id: int
    billing_id: int
    amount: Decimal
    payment_method: str
    status: str
    created_at: datetime


class PaymentDetailResponse(PaymentResponse):
    """Detailed payment response"""
    
    patient_name: str
    invoice_number: str
    billing_total: Decimal
    billing_status: str


# ============================================
# Exports
# ============================================

__all__ = [
    "PaymentCreate",
    "PaymentUpdate",
    "PaymentRefund",
    "PaymentResponse",
    "PaymentListResponse",
    "PaymentDetailResponse",
]
