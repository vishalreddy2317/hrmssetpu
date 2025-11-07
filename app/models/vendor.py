"""
Vendor Model
Service vendors and contractors
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, Index, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, validates
from typing import Optional
import re

from .base import BaseModel


class Vendor(BaseModel):
    """
    Service vendor model
    """
    
    __tablename__ = "vendors"
    
    # Vendor Details
    vendor_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    company_name: Mapped[str] = mapped_column(String(200), nullable=False)
    
    # Service Type
    service_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        comment="maintenance, housekeeping, security, it_services, laundry, catering, waste_disposal"
    )
    
    # Contact
    contact_person: Mapped[str] = mapped_column(String(200), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Address
    address: Mapped[str] = mapped_column(Text, nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    pincode: Mapped[str] = mapped_column(String(20), nullable=False)
    
    # Business Details
    tax_id: Mapped[Optional[str]] = mapped_column(String(50))
    license_number: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Contract
    contract_number: Mapped[Optional[str]] = mapped_column(String(50))
    contract_start_date: Mapped[Optional[str]] = mapped_column(String(20))
    contract_end_date: Mapped[Optional[str]] = mapped_column(String(20))
    contract_value: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Rating
    rating: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='active',
        nullable=False,
        index=True
    )
    
    # Services Description
    services_description: Mapped[Optional[str]] = mapped_column(Text)
    
    # Notes
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5 OR rating IS NULL', name='vendor_valid_rating'),
        Index('idx_vendor_service_type', 'service_type', 'status'),
        {'comment': 'Service vendors and contractors'}
    )
    
    # Validators
    @validates('email')
    def validate_email(self, key, value):
        if value and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise ValueError("Invalid email format")
        return value
    
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['active', 'inactive', 'terminated', 'suspended']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<Vendor(id={self.id}, name='{self.name}', service='{self.service_type}')>"