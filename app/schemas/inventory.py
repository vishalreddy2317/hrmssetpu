"""
Inventory Schemas
"""

from pydantic import BaseModel, Field, validator, condecimal
from typing import Optional
from datetime import datetime
from decimal import Decimal


# Base Schema
class InventoryBase(BaseModel):
    item_code: str = Field(..., max_length=50, description="Unique item code")
    item_name: str = Field(..., max_length=200, description="Item name")
    category: str = Field(..., max_length=100, description="Item category")
    subcategory: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    unit_of_measurement: str = Field(..., max_length=20, description="Unit like pieces, boxes, kg")
    
    @validator('category')
    def validate_category(cls, v):
        valid = ['medical_supplies', 'surgical_supplies', 'consumables', 
                'stationery', 'cleaning', 'food', 'linen', 'ppe']
        if v.lower() not in valid:
            raise ValueError(f"Category must be one of: {', '.join(valid)}")
        return v.lower()


# Create Schema
class InventoryCreate(InventoryBase):
    current_stock: int = Field(default=0, ge=0)
    minimum_stock: int = Field(default=10, ge=0)
    maximum_stock: int = Field(default=1000, ge=0)
    reorder_level: int = Field(default=20, ge=0)
    unit_price: condecimal(max_digits=10, decimal_places=2, ge=0) = Field(..., description="Unit price")
    total_value: condecimal(max_digits=12, decimal_places=2, ge=0) = Field(default=Decimal('0.00'))
    
    supplier_id: Optional[int] = None
    supplier_name: Optional[str] = Field(None, max_length=200)
    storage_location: Optional[str] = Field(None, max_length=200)
    shelf_number: Optional[str] = Field(None, max_length=50)
    
    batch_number: Optional[str] = Field(None, max_length=50)
    manufacturing_date: Optional[str] = Field(None, max_length=20)
    expiry_date: Optional[str] = Field(None, max_length=20)
    
    status: str = Field(default='active', max_length=20)
    is_available: bool = Field(default=True)
    
    barcode: Optional[str] = Field(None, max_length=100)
    sku: Optional[str] = Field(None, max_length=50)
    
    last_restocked_date: Optional[str] = Field(None, max_length=20)
    last_restocked_quantity: Optional[int] = Field(None, ge=0)
    total_consumed: int = Field(default=0, ge=0)
    notes: Optional[str] = None
    
    @validator('status')
    def validate_status(cls, v):
        valid = ['active', 'discontinued', 'expired', 'out_of_stock', 'recalled']
        if v.lower() not in valid:
            raise ValueError(f"Status must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validator('maximum_stock')
    def validate_max_stock(cls, v, values):
        if 'minimum_stock' in values and v < values['minimum_stock']:
            raise ValueError("Maximum stock must be greater than minimum stock")
        return v


# Update Schema
class InventoryUpdate(BaseModel):
    item_name: Optional[str] = Field(None, max_length=200)
    category: Optional[str] = Field(None, max_length=100)
    subcategory: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    unit_of_measurement: Optional[str] = Field(None, max_length=20)
    
    current_stock: Optional[int] = Field(None, ge=0)
    minimum_stock: Optional[int] = Field(None, ge=0)
    maximum_stock: Optional[int] = Field(None, ge=0)
    reorder_level: Optional[int] = Field(None, ge=0)
    
    unit_price: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    total_value: Optional[condecimal(max_digits=12, decimal_places=2, ge=0)] = None
    
    supplier_id: Optional[int] = None
    supplier_name: Optional[str] = Field(None, max_length=200)
    storage_location: Optional[str] = Field(None, max_length=200)
    shelf_number: Optional[str] = Field(None, max_length=50)
    
    batch_number: Optional[str] = Field(None, max_length=50)
    manufacturing_date: Optional[str] = Field(None, max_length=20)
    expiry_date: Optional[str] = Field(None, max_length=20)
    
    status: Optional[str] = Field(None, max_length=20)
    is_available: Optional[bool] = None
    
    barcode: Optional[str] = Field(None, max_length=100)
    sku: Optional[str] = Field(None, max_length=50)
    
    last_restocked_date: Optional[str] = Field(None, max_length=20)
    last_restocked_quantity: Optional[int] = Field(None, ge=0)
    total_consumed: Optional[int] = Field(None, ge=0)
    notes: Optional[str] = None


# Response Schema
class InventoryResponse(InventoryBase):
    id: int
    current_stock: int
    minimum_stock: int
    maximum_stock: int
    reorder_level: int
    unit_price: Decimal
    total_value: Decimal
    
    supplier_id: Optional[int]
    supplier_name: Optional[str]
    storage_location: Optional[str]
    shelf_number: Optional[str]
    
    batch_number: Optional[str]
    manufacturing_date: Optional[str]
    expiry_date: Optional[str]
    
    status: str
    is_available: bool
    
    barcode: Optional[str]
    sku: Optional[str]
    
    last_restocked_date: Optional[str]
    last_restocked_quantity: Optional[int]
    total_consumed: int
    notes: Optional[str]
    
    is_low_stock: bool
    stock_percentage: float
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v)
        }


# List Response
class InventoryListResponse(BaseModel):
    total: int
    items: list[InventoryResponse]
    page: int
    page_size: int
    total_pages: int


# Stock Update Schema
class StockUpdateSchema(BaseModel):
    quantity: int = Field(..., description="Quantity to add (positive) or remove (negative)")
    reason: str = Field(..., max_length=200)
    notes: Optional[str] = None