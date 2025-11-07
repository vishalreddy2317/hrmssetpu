"""
Supplier Schemas
"""

from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional
from datetime import datetime
import re


# Base Schema
class SupplierBase(BaseModel):
    supplier_code: str = Field(..., max_length=50, description="Unique supplier code")
    name: str = Field(..., max_length=200)
    company_name: str = Field(..., max_length=200)
    supplier_type: str = Field(..., max_length=50)
    
    @validator('supplier_type')
    def validate_supplier_type(cls, v):
        valid = [
            'medical_equipment', 'pharmaceutical', 'consumables',
            'general', 'services', 'it', 'food'
        ]
        if v.lower() not in valid:
            raise ValueError(f"Supplier type must be one of: {', '.join(valid)}")
        return v.lower()


# Create Schema
class SupplierCreate(SupplierBase):
    contact_person: str = Field(..., max_length=200)
    phone: str = Field(..., max_length=20)
    alternate_phone: Optional[str] = Field(None, max_length=20)
    email: EmailStr = Field(...)
    website: Optional[str] = Field(None, max_length=200)
    
    address: str = Field(...)
    city: str = Field(..., max_length=100)
    state: str = Field(..., max_length=100)
    country: str = Field(default="USA", max_length=100)
    pincode: str = Field(..., max_length=20)
    
    tax_id: Optional[str] = Field(None, max_length=50)
    license_number: Optional[str] = Field(None, max_length=100)
    registration_number: Optional[str] = Field(None, max_length=100)
    
    bank_name: Optional[str] = Field(None, max_length=200)
    account_number: Optional[str] = Field(None, max_length=50)
    ifsc_code: Optional[str] = Field(None, max_length=20)
    
    rating: Optional[int] = Field(None, ge=1, le=5)
    
    status: str = Field(default='active', max_length=20)
    is_verified: bool = Field(default=False)
    
    payment_terms: Optional[str] = Field(None, max_length=100)
    credit_limit: Optional[int] = Field(None, ge=0)
    
    contract_start_date: Optional[str] = Field(None, max_length=20)
    contract_end_date: Optional[str] = Field(None, max_length=20)
    
    products_supplied: Optional[str] = Field(None, description="JSON array")
    notes: Optional[str] = None
    
    @validator('status')
    def validate_status(cls, v):
        valid = ['active', 'inactive', 'blacklisted', 'on_hold', 'pending_verification']
        if v.lower() not in valid:
            raise ValueError(f"Status must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validator('phone')
    def validate_phone(cls, v):
        if v and not re.match(r'^\+?1?\d{9,15}$', v.replace('-', '').replace(' ', '')):
            raise ValueError("Invalid phone number format")
        return v


# Update Schema
class SupplierUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    company_name: Optional[str] = Field(None, max_length=200)
    supplier_type: Optional[str] = Field(None, max_length=50)
    
    contact_person: Optional[str] = Field(None, max_length=200)
    phone: Optional[str] = Field(None, max_length=20)
    alternate_phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    website: Optional[str] = Field(None, max_length=200)
    
    address: Optional[str] = None
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    pincode: Optional[str] = Field(None, max_length=20)
    
    tax_id: Optional[str] = Field(None, max_length=50)
    license_number: Optional[str] = Field(None, max_length=100)
    registration_number: Optional[str] = Field(None, max_length=100)
    
    bank_name: Optional[str] = Field(None, max_length=200)
    account_number: Optional[str] = Field(None, max_length=50)
    ifsc_code: Optional[str] = Field(None, max_length=20)
    
    rating: Optional[int] = Field(None, ge=1, le=5)
    
    status: Optional[str] = Field(None, max_length=20)
    is_verified: Optional[bool] = None
    
    payment_terms: Optional[str] = Field(None, max_length=100)
    credit_limit: Optional[int] = Field(None, ge=0)
    
    contract_start_date: Optional[str] = Field(None, max_length=20)
    contract_end_date: Optional[str] = Field(None, max_length=20)
    
    products_supplied: Optional[str] = None
    notes: Optional[str] = None


# Response Schema
class SupplierResponse(SupplierBase):
    id: int
    
    contact_person: str
    phone: str
    alternate_phone: Optional[str]
    email: str
    website: Optional[str]
    
    address: str
    city: str
    state: str
    country: str
    pincode: str
    
    tax_id: Optional[str]
    license_number: Optional[str]
    registration_number: Optional[str]
    
    bank_name: Optional[str]
    account_number: Optional[str]
    ifsc_code: Optional[str]
    
    rating: Optional[int]
    
    status: str
    is_verified: bool
    
    payment_terms: Optional[str]
    credit_limit: Optional[int]
    
    contract_start_date: Optional[str]
    contract_end_date: Optional[str]
    
    products_supplied: Optional[str]
    notes: Optional[str]
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# List Response
class SupplierListResponse(BaseModel):
    total: int
    items: list[SupplierResponse]
    page: int
    page_size: int
    total_pages: int


# Supplier with Performance
class SupplierWithPerformanceResponse(SupplierResponse):
    total_orders: int
    total_amount: float
    on_time_delivery_rate: float
    quality_rating: float
    last_order_date: Optional[str]


# Supplier Filter Schema
class SupplierFilterSchema(BaseModel):
    supplier_type: Optional[str] = Field(None, max_length=50)
    status: Optional[str] = Field(None, max_length=20)
    is_verified: Optional[bool] = None
    
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    
    min_rating: Optional[int] = Field(None, ge=1, le=5)
    payment_terms: Optional[str] = Field(None, max_length=100)


# Supplier Evaluation Schema
class SupplierEvaluationSchema(BaseModel):
    supplier_id: int = Field(..., gt=0)
    
    evaluation_date: str = Field(..., max_length=20)
    evaluation_period: str = Field(..., description="quarterly, half_yearly, annual")
    
    # Criteria (1-5 scale)
    quality_rating: int = Field(..., ge=1, le=5)
    delivery_rating: int = Field(..., ge=1, le=5)
    pricing_rating: int = Field(..., ge=1, le=5)
    service_rating: int = Field(..., ge=1, le=5)
    documentation_rating: int = Field(..., ge=1, le=5)
    
    # Metrics
    total_orders: int
    on_time_deliveries: int
    quality_issues: int
    price_competitiveness: str = Field(..., description="excellent, good, average, poor")
    
    # Comments
    strengths: Optional[str] = None
    weaknesses: Optional[str] = None
    recommendations: Optional[str] = None
    
    overall_rating: float
    
    evaluated_by: str = Field(..., max_length=200)
    
    @validator('evaluation_period')
    def validate_period(cls, v):
        valid = ['monthly', 'quarterly', 'half_yearly', 'annual']
        if v.lower() not in valid:
            raise ValueError(f"Evaluation period must be one of: {', '.join(valid)}")
        return v.lower()


# Supplier Performance Report
class SupplierPerformanceReportSchema(BaseModel):
    supplier_id: int
    supplier_name: str
    
    period_start: str
    period_end: str
    
    total_purchase_orders: int
    total_amount: float
    
    on_time_deliveries: int
    delayed_deliveries: int
    on_time_delivery_percentage: float
    
    quality_issues_count: int
    returns_count: int
    
    average_delivery_days: float
    average_rating: float
    
    payment_compliance: str
    
    top_products: list[dict]


# Supplier Comparison Schema
class SupplierComparisonSchema(BaseModel):
    supplier_ids: list[int] = Field(..., min_items=2, max_items=5)
    comparison_criteria: list[str] = Field(..., min_items=1)
    period_start: Optional[str] = Field(None, max_length=20)
    period_end: Optional[str] = Field(None, max_length=20)


# Supplier Comparison Response
class SupplierComparisonResponse(BaseModel):
    suppliers: list[dict]  # Supplier details and metrics
    comparison_matrix: dict  # {criterion: {supplier_id: value}}
    best_in_category: dict  # {criterion: supplier_id}
    recommendations: str


# Supplier Product Schema
class SupplierProductSchema(BaseModel):
    supplier_id: int = Field(..., gt=0)
    
    product_name: str = Field(..., max_length=200)
    product_code: str = Field(..., max_length=50)
    category: str = Field(..., max_length=100)
    
    unit_price: float = Field(..., gt=0)
    minimum_order_quantity: int = Field(default=1, ge=1)
    
    lead_time_days: int = Field(..., ge=0)
    
    is_available: bool = Field(default=True)
    notes: Optional[str] = None


# Supplier Payment History
class SupplierPaymentHistorySchema(BaseModel):
    supplier_id: int
    supplier_name: str
    
    total_invoices: int
    total_amount_due: float
    total_amount_paid: float
    outstanding_amount: float
    
    on_time_payments: int
    delayed_payments: int
    
    payment_history: list[dict]  # {invoice_no, amount, due_date, paid_date, status}
    
    average_payment_delay_days: float
    credit_utilization_percentage: float