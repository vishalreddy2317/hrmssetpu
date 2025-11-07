"""
Supplier Model
Supplier and vendor management for inventory
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, Index, CheckConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional, List
import re

from .base import BaseModel


class Supplier(BaseModel):
    """
    Supplier/Vendor model
    """
    
    __tablename__ = "suppliers"
    
    # Supplier Details
    supplier_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    company_name: Mapped[str] = mapped_column(String(200), nullable=False)
    
    # Type
    supplier_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        comment="medical_equipment, pharmaceutical, consumables, general, services"
    )
    
    # Contact Information
    contact_person: Mapped[str] = mapped_column(String(200), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    alternate_phone: Mapped[Optional[str]] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    website: Mapped[Optional[str]] = mapped_column(String(200))
    
    # Address
    address: Mapped[str] = mapped_column(Text, nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), default="USA")
    pincode: Mapped[str] = mapped_column(String(20), nullable=False)
    
    # Business Details
    tax_id: Mapped[Optional[str]] = mapped_column(String(50), unique=True)
    license_number: Mapped[Optional[str]] = mapped_column(String(100))
    registration_number: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Bank Details
    bank_name: Mapped[Optional[str]] = mapped_column(String(200))
    account_number: Mapped[Optional[str]] = mapped_column(String(50))
    ifsc_code: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Rating
    rating: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='active',
        nullable=False,
        index=True,
        comment="active, inactive, blacklisted, on_hold"
    )
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Payment Terms
    payment_terms: Mapped[Optional[str]] = mapped_column(String(100), comment="net_30, net_60, advance, cod")
    credit_limit: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Contract
    contract_start_date: Mapped[Optional[str]] = mapped_column(String(20))
    contract_end_date: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Products Supplied
    products_supplied: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array")
    
    # Notes
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationships
    purchase_orders: Mapped[List["PurchaseOrder"]] = relationship(
        "PurchaseOrder",
        back_populates="supplier",
        lazy="dynamic"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5 OR rating IS NULL', name='supplier_valid_rating'),
        Index('idx_supplier_type', 'supplier_type', 'status'),
        {'comment': 'Supplier and vendor management'}
    )
    
    # Validators
    @validates('email')
    def validate_email(self, key, value):
        if value and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise ValueError("Invalid email format")
        return value
    
    @validates('supplier_type')
    def validate_supplier_type(self, key, value):
        valid_types = [
            'medical_equipment', 'pharmaceutical', 'consumables',
            'general', 'services', 'it', 'food'
        ]
        if value.lower() not in valid_types:
            raise ValueError(f"Supplier type must be one of: {', '.join(valid_types)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['active', 'inactive', 'blacklisted', 'on_hold', 'pending_verification']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<Supplier(id={self.id}, name='{self.name}', code='{self.supplier_code}')>"
    