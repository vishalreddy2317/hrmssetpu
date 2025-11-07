"""
Vendor Schemas
"""

from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional
from datetime import datetime
import re


# Base Schema
class VendorBase(BaseModel):
    vendor_code: str = Field(..., max_length=50, description="Unique vendor code")
    name: str = Field(..., max_length=200)
    company_name: str = Field(..., max_length=200)
    service_type: str = Field(..., max_length=100)
    
    @validator('service_type')
    def validate_service_type(cls, v):
        valid = [
            'maintenance', 'housekeeping', 'security', 'it_services',
            'laundry', 'catering', 'waste_disposal', 'biomedical', 'transport'
        ]
        if v.lower() not in valid:
            raise ValueError(f"Service type must be one of: {', '.join(valid)}")
        return v.lower()


# Create Schema
class VendorCreate(VendorBase):
    contact_person: str = Field(..., max_length=200)
    phone: str = Field(..., max_length=20)
    email: EmailStr = Field(...)
    
    address: str = Field(...)
    city: str = Field(..., max_length=100)
    state: str = Field(..., max_length=100)
    pincode: str = Field(..., max_length=20)
    
    tax_id: Optional[str] = Field(None, max_length=50)
    license_number: Optional[str] = Field(None, max_length=100)
    
    contract_number: Optional[str] = Field(None, max_length=50)
    contract_start_date: Optional[str] = Field(None, max_length=20)
    contract_end_date: Optional[str] = Field(None, max_length=20)
    contract_value: Optional[int] = Field(None, ge=0)
    
    rating: Optional[int] = Field(None, ge=1, le=5)
    
    status: str = Field(default='active', max_length=20)
    
    services_description: Optional[str] = None
    notes: Optional[str] = None
    
    @validator('status')
    def validate_status(cls, v):
        valid = ['active', 'inactive', 'terminated', 'suspended']
        if v.lower() not in valid:
            raise ValueError(f"Status must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validator('phone')
    def validate_phone(cls, v):
        if v and not re.match(r'^\+?1?\d{9,15}$', v.replace('-', '').replace(' ', '')):
            raise ValueError("Invalid phone number format")
        return v


# Update Schema
class VendorUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    company_name: Optional[str] = Field(None, max_length=200)
    service_type: Optional[str] = Field(None, max_length=100)
    
    contact_person: Optional[str] = Field(None, max_length=200)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    
    address: Optional[str] = None
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    pincode: Optional[str] = Field(None, max_length=20)
    
    tax_id: Optional[str] = Field(None, max_length=50)
    license_number: Optional[str] = Field(None, max_length=100)
    
    contract_number: Optional[str] = Field(None, max_length=50)
    contract_start_date: Optional[str] = Field(None, max_length=20)
    contract_end_date: Optional[str] = Field(None, max_length=20)
    contract_value: Optional[int] = Field(None, ge=0)
    
    rating: Optional[int] = Field(None, ge=1, le=5)
    status: Optional[str] = Field(None, max_length=20)
    
    services_description: Optional[str] = None
    notes: Optional[str] = None


# Response Schema
class VendorResponse(VendorBase):
    id: int
    
    contact_person: str
    phone: str
    email: str
    
    address: str
    city: str
    state: str
    pincode: str
    
    tax_id: Optional[str]
    license_number: Optional[str]
    
    contract_number: Optional[str]
    contract_start_date: Optional[str]
    contract_end_date: Optional[str]
    contract_value: Optional[int]
    
    rating: Optional[int]
    status: str
    
    services_description: Optional[str]
    notes: Optional[str]
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# List Response
class VendorListResponse(BaseModel):
    total: int
    items: list[VendorResponse]
    page: int
    page_size: int
    total_pages: int