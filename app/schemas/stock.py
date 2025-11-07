"""
Stock Schemas
"""

from pydantic import BaseModel, Field, validator, condecimal
from typing import Optional
from datetime import datetime
from decimal import Decimal


# Base Schema
class StockBase(BaseModel):
    transaction_number: str = Field(..., max_length=20, description="Unique transaction number")
    transaction_date: str = Field(..., max_length=20)
    item_name: str = Field(..., max_length=200)
    transaction_type: str = Field(..., max_length=50)
    
    @validator('transaction_type')
    def validate_transaction_type(cls, v):
        valid = [
            'purchase', 'sale', 'return', 'adjustment', 'transfer',
            'damage', 'expiry', 'disposal', 'opening_stock'
        ]
        if v.lower() not in valid:
            raise ValueError(f"Transaction type must be one of: {', '.join(valid)}")
        return v.lower()


# Create Schema
class StockCreate(StockBase):
    medicine_id: Optional[int] = None
    inventory_id: Optional[int] = None
    
    item_code: Optional[str] = Field(None, max_length=50)
    
    quantity: int = Field(..., description="Quantity (positive for in, negative for out)")
    unit_of_measurement: str = Field(default='units', max_length=20)
    
    previous_stock: int = Field(..., ge=0)
    new_stock: int = Field(..., ge=0)
    
    unit_price: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    total_amount: Optional[condecimal(max_digits=12, decimal_places=2, ge=0)] = None
    
    batch_number: Optional[str] = Field(None, max_length=50)
    manufacturing_date: Optional[str] = Field(None, max_length=20)
    expiry_date: Optional[str] = Field(None, max_length=20)
    
    purchase_order_id: Optional[int] = None
    supplier_id: Optional[int] = None
    
    from_location: Optional[str] = Field(None, max_length=100)
    to_location: Optional[str] = Field(None, max_length=100)
    
    performed_by: str = Field(..., max_length=200)
    approved_by: Optional[str] = Field(None, max_length=200)
    
    reason: Optional[str] = None
    notes: Optional[str] = None
    
    status: str = Field(default='completed', max_length=20)
    
    @validator('quantity')
    def validate_quantity(cls, v):
        if v == 0:
            raise ValueError("Quantity cannot be zero")
        return v
    
    @validator('status')
    def validate_status(cls, v):
        valid = ['pending', 'completed', 'cancelled', 'reversed']
        if v.lower() not in valid:
            raise ValueError(f"Status must be one of: {', '.join(valid)}")
        return v.lower()


# Update Schema
class StockUpdate(BaseModel):
    transaction_date: Optional[str] = Field(None, max_length=20)
    
    batch_number: Optional[str] = Field(None, max_length=50)
    manufacturing_date: Optional[str] = Field(None, max_length=20)
    expiry_date: Optional[str] = Field(None, max_length=20)
    
    unit_price: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    total_amount: Optional[condecimal(max_digits=12, decimal_places=2, ge=0)] = None
    
    approved_by: Optional[str] = Field(None, max_length=200)
    reason: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = Field(None, max_length=20)


# Response Schema
class StockResponse(StockBase):
    id: int
    medicine_id: Optional[int]
    inventory_id: Optional[int]
    
    item_code: Optional[str]
    
    quantity: int
    unit_of_measurement: str
    
    previous_stock: int
    new_stock: int
    quantity_change: int
    
    unit_price: Optional[Decimal]
    total_amount: Optional[Decimal]
    
    batch_number: Optional[str]
    manufacturing_date: Optional[str]
    expiry_date: Optional[str]
    
    purchase_order_id: Optional[int]
    supplier_id: Optional[int]
    
    from_location: Optional[str]
    to_location: Optional[str]
    
    performed_by: str
    approved_by: Optional[str]
    
    reason: Optional[str]
    notes: Optional[str]
    
    status: str
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v)
        }


# List Response
class StockListResponse(BaseModel):
    total: int
    items: list[StockResponse]
    page: int
    page_size: int
    total_pages: int


# Stock Filter Schema
class StockFilterSchema(BaseModel):
    medicine_id: Optional[int] = None
    inventory_id: Optional[int] = None
    
    transaction_type: Optional[str] = Field(None, max_length=50)
    status: Optional[str] = Field(None, max_length=20)
    
    start_date: Optional[str] = Field(None, max_length=20)
    end_date: Optional[str] = Field(None, max_length=20)
    
    batch_number: Optional[str] = Field(None, max_length=50)
    supplier_id: Optional[int] = None
    
    from_location: Optional[str] = Field(None, max_length=100)
    to_location: Optional[str] = Field(None, max_length=100)


# Stock Summary Schema
class StockSummarySchema(BaseModel):
    item_id: int
    item_name: str
    item_code: Optional[str]
    
    current_stock: int
    total_purchases: int
    total_sales: int
    total_returns: int
    total_adjustments: int
    total_damaged: int
    total_expired: int
    
    stock_value: Decimal
    
    last_transaction_date: Optional[str]
    last_transaction_type: Optional[str]
    
    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }


# Stock Alert Schema
class StockAlertSchema(BaseModel):
    item_id: int
    item_name: str
    item_code: Optional[str]
    
    current_stock: int
    reorder_level: int
    minimum_stock: int
    
    alert_type: str = Field(..., description="low_stock, out_of_stock, expiring_soon, expired")
    alert_level: str = Field(..., description="warning, critical")
    
    expiry_date: Optional[str]
    days_to_expiry: Optional[int]
    
    recommended_order_quantity: Optional[int]


# Stock Transfer Schema
class StockTransferSchema(BaseModel):
    item_id: int
    item_type: str = Field(..., description="medicine, inventory")
    
    quantity: int = Field(..., gt=0)
    
    from_location: str = Field(..., max_length=100)
    to_location: str = Field(..., max_length=100)
    
    transfer_date: str = Field(..., max_length=20)
    transfer_reason: str = Field(...)
    
    batch_number: Optional[str] = Field(None, max_length=50)
    
    performed_by: str = Field(..., max_length=200)
    approved_by: str = Field(..., max_length=200)
    notes: Optional[str] = None


# Stock Adjustment Schema
class StockAdjustmentSchema(BaseModel):
    item_id: int
    item_type: str = Field(..., description="medicine, inventory")
    
    adjustment_quantity: int = Field(..., description="Positive or negative")
    adjustment_reason: str = Field(...)
    
    current_stock: int = Field(..., ge=0)
    new_stock: int = Field(..., ge=0)
    
    adjusted_by: str = Field(..., max_length=200)
    approved_by: str = Field(..., max_length=200)
    
    batch_number: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = None


# Stock Valuation Schema
class StockValuationSchema(BaseModel):
    total_items: int
    total_stock_quantity: int
    total_stock_value: Decimal
    
    by_category: dict  # {category: {quantity, value}}
    by_location: dict  # {location: {quantity, value}}
    
    low_stock_items: int
    out_of_stock_items: int
    expiring_soon_items: int
    
    valuation_date: str
    
    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }


# Stock History Schema
class StockHistorySchema(BaseModel):
    item_id: int
    item_name: str
    
    period_start: str
    period_end: str
    
    opening_stock: int
    closing_stock: int
    
    total_in: int
    total_out: int
    net_change: int
    
    transactions: list[StockResponse]


# Expiring Stock Schema
class ExpiringStockSchema(BaseModel):
    item_id: int
    item_name: str
    item_code: Optional[str]
    
    batch_number: str
    expiry_date: str
    days_to_expiry: int
    
    quantity: int
    value: Decimal
    location: Optional[str]
    
    urgency: str = Field(..., description="expired, critical, warning, normal")
    
    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }


# Stock Report Schema
class StockReportSchema(BaseModel):
    report_type: str = Field(..., description="daily, weekly, monthly, custom")
    report_date: str
    
    period_start: str
    period_end: str
    
    total_transactions: int
    total_purchases: int
    total_sales: int
    total_value_in: Decimal
    total_value_out: Decimal
    
    by_transaction_type: dict  # {type: {count, quantity, value}}
    by_category: dict
    
    top_moving_items: list[dict]
    slow_moving_items: list[dict]
    
    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }