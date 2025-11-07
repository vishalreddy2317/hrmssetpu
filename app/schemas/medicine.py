"""
Medicine Schemas
"""

from pydantic import BaseModel, Field, validator, condecimal
from typing import Optional
from datetime import datetime
from decimal import Decimal


# Base Schema
class MedicineBase(BaseModel):
    medicine_code: str = Field(..., max_length=50, description="Unique medicine code")
    name: str = Field(..., max_length=200)
    generic_name: str = Field(..., max_length=200)
    brand_name: Optional[str] = Field(None, max_length=200)
    
    category: str = Field(..., max_length=100)
    drug_class: Optional[str] = Field(None, max_length=100)
    
    dosage_form: str = Field(..., max_length=50)
    strength: str = Field(..., max_length=50)
    unit: str = Field(..., max_length=20)
    
    manufacturer: str = Field(..., max_length=200)
    
    @validator('dosage_form')
    def validate_dosage_form(cls, v):
        valid = ['tablet', 'capsule', 'syrup', 'injection', 'ointment',
                'cream', 'drops', 'inhaler', 'patch', 'powder', 'solution']
        if v.lower() not in valid:
            raise ValueError(f"Dosage form must be one of: {', '.join(valid)}")
        return v.lower()


# Create Schema
class MedicineCreate(MedicineBase):
    supplier: Optional[str] = Field(None, max_length=200)
    
    stock_quantity: int = Field(default=0, ge=0)
    reorder_level: int = Field(default=10, ge=0)
    unit_of_measurement: str = Field(default='units', max_length=20)
    
    purchase_price: condecimal(max_digits=10, decimal_places=2, gt=0) = Field(...)
    selling_price: condecimal(max_digits=10, decimal_places=2, gt=0) = Field(...)
    mrp: Optional[condecimal(max_digits=10, decimal_places=2, gt=0)] = None
    
    batch_number: Optional[str] = Field(None, max_length=50)
    manufacturing_date: Optional[str] = Field(None, max_length=20)
    expiry_date: Optional[str] = Field(None, max_length=20)
    
    requires_prescription: bool = Field(default=True)
    is_controlled_substance: bool = Field(default=False)
    schedule_category: Optional[str] = Field(None, max_length=20)
    
    usage_instructions: Optional[str] = None
    dosage_instructions: Optional[str] = None
    side_effects: Optional[str] = None
    contraindications: Optional[str] = None
    warnings: Optional[str] = None
    
    storage_conditions: Optional[str] = Field(None, max_length=200)
    storage_location: Optional[str] = Field(None, max_length=100)
    
    status: str = Field(default='active', max_length=20)
    is_available: bool = Field(default=True)
    
    description: Optional[str] = None
    barcode: Optional[str] = Field(None, max_length=100)
    
    @validator('status')
    def validate_status(cls, v):
        valid = ['active', 'discontinued', 'out_of_stock', 'expired', 'recalled']
        if v.lower() not in valid:
            raise ValueError(f"Status must be one of: {', '.join(valid)}")
        return v.lower()


# Update Schema
class MedicineUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    generic_name: Optional[str] = Field(None, max_length=200)
    brand_name: Optional[str] = Field(None, max_length=200)
    
    category: Optional[str] = Field(None, max_length=100)
    drug_class: Optional[str] = Field(None, max_length=100)
    
    dosage_form: Optional[str] = Field(None, max_length=50)
    strength: Optional[str] = Field(None, max_length=50)
    unit: Optional[str] = Field(None, max_length=20)
    
    manufacturer: Optional[str] = Field(None, max_length=200)
    supplier: Optional[str] = Field(None, max_length=200)
    
    stock_quantity: Optional[int] = Field(None, ge=0)
    reorder_level: Optional[int] = Field(None, ge=0)
    
    purchase_price: Optional[condecimal(max_digits=10, decimal_places=2, gt=0)] = None
    selling_price: Optional[condecimal(max_digits=10, decimal_places=2, gt=0)] = None
    mrp: Optional[condecimal(max_digits=10, decimal_places=2, gt=0)] = None
    
    batch_number: Optional[str] = Field(None, max_length=50)
    manufacturing_date: Optional[str] = Field(None, max_length=20)
    expiry_date: Optional[str] = Field(None, max_length=20)
    
    requires_prescription: Optional[bool] = None
    is_controlled_substance: Optional[bool] = None
    schedule_category: Optional[str] = Field(None, max_length=20)
    
    usage_instructions: Optional[str] = None
    dosage_instructions: Optional[str] = None
    side_effects: Optional[str] = None
    contraindications: Optional[str] = None
    warnings: Optional[str] = None
    
    storage_conditions: Optional[str] = Field(None, max_length=200)
    storage_location: Optional[str] = Field(None, max_length=100)
    
    status: Optional[str] = Field(None, max_length=20)
    is_available: Optional[bool] = None
    
    description: Optional[str] = None
    barcode: Optional[str] = Field(None, max_length=100)


# Response Schema
class MedicineResponse(MedicineBase):
    id: int
    supplier: Optional[str]
    
    stock_quantity: int
    reorder_level: int
    unit_of_measurement: str
    
    purchase_price: Decimal
    selling_price: Decimal
    mrp: Optional[Decimal]
    
    batch_number: Optional[str]
    manufacturing_date: Optional[str]
    expiry_date: Optional[str]
    
    requires_prescription: bool
    is_controlled_substance: bool
    schedule_category: Optional[str]
    
    usage_instructions: Optional[str]
    dosage_instructions: Optional[str]
    side_effects: Optional[str]
    contraindications: Optional[str]
    warnings: Optional[str]
    
    storage_conditions: Optional[str]
    storage_location: Optional[str]
    
    status: str
    is_available: bool
    
    description: Optional[str]
    barcode: Optional[str]
    
    is_low_stock: bool
    profit_margin: Decimal
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v)
        }


# List Response
class MedicineListResponse(BaseModel):
    total: int
    items: list[MedicineResponse]
    page: int
    page_size: int
    total_pages: int


# Stock Update Schema
class MedicineStockUpdate(BaseModel):
    quantity: int = Field(..., description="Quantity to add (positive) or remove (negative)")
    batch_number: Optional[str] = Field(None, max_length=50)
    manufacturing_date: Optional[str] = Field(None, max_length=20)
    expiry_date: Optional[str] = Field(None, max_length=20)
    reason: str = Field(..., max_length=200)
    notes: Optional[str] = None