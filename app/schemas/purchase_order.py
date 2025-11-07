"""
Purchase Order Schemas
"""

from pydantic import BaseModel, Field, validator, condecimal
from typing import Optional
from datetime import datetime
from decimal import Decimal


# Base Schema
class PurchaseOrderBase(BaseModel):
    po_number: str = Field(..., max_length=20, description="Unique PO number")
    po_date: str = Field(..., max_length=20)
    supplier_id: int = Field(..., gt=0)


# Create Schema
class PurchaseOrderCreate(PurchaseOrderBase):
    items: str = Field(..., description="JSON array of items")
    
    subtotal: condecimal(max_digits=12, decimal_places=2, ge=0) = Field(...)
    tax_amount: condecimal(max_digits=12, decimal_places=2, ge=0) = Field(default=Decimal('0.00'))
    shipping_cost: condecimal(max_digits=10, decimal_places=2, ge=0) = Field(default=Decimal('0.00'))
    discount_amount: condecimal(max_digits=10, decimal_places=2, ge=0) = Field(default=Decimal('0.00'))
    total_amount: condecimal(max_digits=12, decimal_places=2, ge=0) = Field(...)
    
    expected_delivery_date: Optional[str] = Field(None, max_length=20)
    actual_delivery_date: Optional[str] = Field(None, max_length=20)
    delivery_address: str = Field(...)
    
    status: str = Field(default='pending', max_length=20)
    payment_status: str = Field(default='pending', max_length=20)
    payment_terms: Optional[str] = Field(None, max_length=100)
    
    requested_by: str = Field(..., max_length=200)
    approved_by: Optional[str] = Field(None, max_length=200)
    approved_date: Optional[str] = Field(None, max_length=20)
    
    notes: Optional[str] = None
    terms_conditions: Optional[str] = None
    
    @validator('status')
    def validate_status(cls, v):
        valid = ['pending', 'approved', 'rejected', 'ordered', 
                'partially_received', 'received', 'cancelled']
        if v.lower() not in valid:
            raise ValueError(f"Status must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validator('payment_status')
    def validate_payment_status(cls, v):
        valid = ['pending', 'partial', 'paid']
        if v.lower() not in valid:
            raise ValueError(f"Payment status must be one of: {', '.join(valid)}")
        return v.lower()


# Update Schema
class PurchaseOrderUpdate(BaseModel):
    items: Optional[str] = None
    
    subtotal: Optional[condecimal(max_digits=12, decimal_places=2, ge=0)] = None
    tax_amount: Optional[condecimal(max_digits=12, decimal_places=2, ge=0)] = None
    shipping_cost: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    discount_amount: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    total_amount: Optional[condecimal(max_digits=12, decimal_places=2, ge=0)] = None
    
    expected_delivery_date: Optional[str] = Field(None, max_length=20)
    actual_delivery_date: Optional[str] = Field(None, max_length=20)
    delivery_address: Optional[str] = None
    
    status: Optional[str] = Field(None, max_length=20)
    payment_status: Optional[str] = Field(None, max_length=20)
    payment_terms: Optional[str] = Field(None, max_length=100)
    
    approved_by: Optional[str] = Field(None, max_length=200)
    approved_date: Optional[str] = Field(None, max_length=20)
    
    notes: Optional[str] = None
    terms_conditions: Optional[str] = None


# Response Schema
class PurchaseOrderResponse(PurchaseOrderBase):
    id: int
    items: str
    
    subtotal: Decimal
    tax_amount: Decimal
    shipping_cost: Decimal
    discount_amount: Decimal
    total_amount: Decimal
    
    expected_delivery_date: Optional[str]
    actual_delivery_date: Optional[str]
    delivery_address: str
    
    status: str
    payment_status: str
    payment_terms: Optional[str]
    
    requested_by: str
    approved_by: Optional[str]
    approved_date: Optional[str]
    
    notes: Optional[str]
    terms_conditions: Optional[str]
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v)
        }


# List Response
class PurchaseOrderListResponse(BaseModel):
    total: int
    items: list[PurchaseOrderResponse]
    page: int
    page_size: int
    total_pages: int


# PO Item Schema
class PurchaseOrderItemSchema(BaseModel):
    item_name: str = Field(..., max_length=200)
    item_code: Optional[str] = Field(None, max_length=50)
    quantity: int = Field(..., gt=0)
    unit_price: condecimal(max_digits=10, decimal_places=2, ge=0) = Field(...)
    total_price: condecimal(max_digits=10, decimal_places=2, ge=0) = Field(...)
    description: Optional[str] = None


# Approve PO Schema
class PurchaseOrderApproveSchema(BaseModel):
    approved_by: str = Field(..., max_length=200)
    approved_date: str = Field(..., max_length=20)
    notes: Optional[str] = None


# Receive PO Schema
class PurchaseOrderReceiveSchema(BaseModel):
    actual_delivery_date: str = Field(..., max_length=20)
    items_received: str = Field(..., description="JSON array of received items with quantities")
    notes: Optional[str] = None