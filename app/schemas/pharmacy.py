"""
Pharmacy Schemas
"""

from pydantic import BaseModel, Field, validator, condecimal
from typing import Optional
from datetime import datetime
from decimal import Decimal


# Base Schema
class PharmacyBase(BaseModel):
    transaction_number: str = Field(..., max_length=20, description="Unique transaction number")
    transaction_date: str = Field(..., max_length=20)
    transaction_time: str = Field(..., max_length=10)


# Create Schema
class PharmacyCreate(PharmacyBase):
    prescription_id: Optional[int] = None
    patient_id: int = Field(..., gt=0)
    
    medicines_dispensed: str = Field(..., description="JSON array of medicines")
    
    dispensed_by: str = Field(..., max_length=200)
    pharmacist_id: Optional[int] = None
    
    total_amount: condecimal(max_digits=10, decimal_places=2, ge=0) = Field(...)
    discount_amount: condecimal(max_digits=10, decimal_places=2, ge=0) = Field(default=Decimal('0.00'))
    tax_amount: condecimal(max_digits=10, decimal_places=2, ge=0) = Field(default=Decimal('0.00'))
    final_amount: condecimal(max_digits=10, decimal_places=2, ge=0) = Field(...)
    
    payment_status: str = Field(default='pending', max_length=20)
    payment_method: Optional[str] = Field(None, max_length=50)
    
    status: str = Field(default='completed', max_length=20)
    
    is_returned: bool = Field(default=False)
    return_date: Optional[str] = Field(None, max_length=20)
    return_reason: Optional[str] = None
    refund_amount: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    
    notes: Optional[str] = None
    
    @validator('payment_status')
    def validate_payment_status(cls, v):
        valid = ['pending', 'paid', 'partially_paid', 'insurance_claimed', 'refunded']
        if v.lower() not in valid:
            raise ValueError(f"Payment status must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validator('status')
    def validate_status(cls, v):
        valid = ['completed', 'cancelled', 'returned', 'partially_returned']
        if v.lower() not in valid:
            raise ValueError(f"Status must be one of: {', '.join(valid)}")
        return v.lower()


# Update Schema
class PharmacyUpdate(BaseModel):
    medicines_dispensed: Optional[str] = None
    
    total_amount: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    discount_amount: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    tax_amount: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    final_amount: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    
    payment_status: Optional[str] = Field(None, max_length=20)
    payment_method: Optional[str] = Field(None, max_length=50)
    
    status: Optional[str] = Field(None, max_length=20)
    
    is_returned: Optional[bool] = None
    return_date: Optional[str] = Field(None, max_length=20)
    return_reason: Optional[str] = None
    refund_amount: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    
    notes: Optional[str] = None


# Response Schema
class PharmacyResponse(PharmacyBase):
    id: int
    prescription_id: Optional[int]
    patient_id: int
    
    medicines_dispensed: str
    
    dispensed_by: str
    pharmacist_id: Optional[int]
    
    total_amount: Decimal
    discount_amount: Decimal
    tax_amount: Decimal
    final_amount: Decimal
    
    payment_status: str
    payment_method: Optional[str]
    
    status: str
    
    is_returned: bool
    return_date: Optional[str]
    return_reason: Optional[str]
    refund_amount: Optional[Decimal]
    
    notes: Optional[str]
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v)
        }


# List Response
class PharmacyListResponse(BaseModel):
    total: int
    items: list[PharmacyResponse]
    page: int
    page_size: int
    total_pages: int


# Return Medicine Schema
class PharmacyReturnSchema(BaseModel):
    return_date: str = Field(..., max_length=20)
    return_reason: str = Field(..., description="Reason for return")
    refund_amount: condecimal(max_digits=10, decimal_places=2, ge=0) = Field(...)
    medicines_returned: str = Field(..., description="JSON array of medicines returned")