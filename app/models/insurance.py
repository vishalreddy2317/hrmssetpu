"""
Insurance Model
Patient insurance information and claims
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional
from decimal import Decimal

from .base import BaseModel


class Insurance(BaseModel):
    """
    Patient insurance and claims model
    """
    
    __tablename__ = "insurances"
    
    # Insurance Details
    insurance_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    policy_number: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    
    # Patient
    patient_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Insurance Provider
    provider_name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    provider_code: Mapped[Optional[str]] = mapped_column(String(50))
    provider_phone: Mapped[Optional[str]] = mapped_column(String(20))
    provider_email: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Policy Details
    policy_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="individual, family, group, corporate, government"
    )
    plan_name: Mapped[str] = mapped_column(String(200), nullable=False)
    
    # Coverage
    coverage_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    used_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal('0.00'))
    remaining_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    
    # Validity
    start_date: Mapped[str] = mapped_column(String(20), nullable=False)
    end_date: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    
    # Policy Holder (if different from patient)
    policy_holder_name: Mapped[str] = mapped_column(String(200), nullable=False)
    policy_holder_relation: Mapped[Optional[str]] = mapped_column(String(50))
    policy_holder_dob: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Co-payment
    copay_percentage: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2))
    copay_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    
    # Deductible
    annual_deductible: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    deductible_met: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal('0.00'))
    
    # Coverage Details
    inpatient_coverage: Mapped[bool] = mapped_column(Boolean, default=True)
    outpatient_coverage: Mapped[bool] = mapped_column(Boolean, default=True)
    emergency_coverage: Mapped[bool] = mapped_column(Boolean, default=True)
    maternity_coverage: Mapped[bool] = mapped_column(Boolean, default=False)
    dental_coverage: Mapped[bool] = mapped_column(Boolean, default=False)
    vision_coverage: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Pre-existing Conditions
    pre_existing_covered: Mapped[bool] = mapped_column(Boolean, default=False)
    waiting_period_months: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Network
    network_type: Mapped[Optional[str]] = mapped_column(String(50), comment="PPO, HMO, EPO, POS")
    is_network_hospital: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Claims
    total_claims: Mapped[int] = mapped_column(Integer, default=0)
    approved_claims: Mapped[int] = mapped_column(Integer, default=0)
    rejected_claims: Mapped[int] = mapped_column(Integer, default=0)
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='active',
        nullable=False,
        index=True,
        comment="active, expired, cancelled, suspended"
    )
    
    # Documents
    policy_document_url: Mapped[Optional[str]] = mapped_column(String(500))
    id_card_url: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Notes
    notes: Mapped[Optional[str]] = mapped_column(Text)
    exclusions: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationships
    patient: Mapped["Patient"] = relationship(
        "Patient",
        backref="insurances"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('coverage_amount > 0', name='insurance_positive_coverage'),
        CheckConstraint('used_amount >= 0', name='insurance_positive_used'),
        CheckConstraint('remaining_amount >= 0', name='insurance_positive_remaining'),
        CheckConstraint('copay_percentage >= 0 AND copay_percentage <= 100 OR copay_percentage IS NULL', name='insurance_valid_copay_percentage'),
        Index('idx_insurance_patient', 'patient_id', 'status'),
        Index('idx_insurance_provider', 'provider_name', 'status'),
        Index('idx_insurance_expiry', 'end_date', 'status'),
        {'comment': 'Patient insurance policies and coverage'}
    )
    
    # Validators
    @validates('policy_type')
    def validate_policy_type(self, key, value):
        valid_types = ['individual', 'family', 'group', 'corporate', 'government', 'senior_citizen']
        if value.lower() not in valid_types:
            raise ValueError(f"Policy type must be one of: {', '.join(valid_types)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['active', 'expired', 'cancelled', 'suspended', 'pending_renewal']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    @property
    def utilization_percentage(self) -> Decimal:
        """Calculate coverage utilization percentage"""
        if self.coverage_amount > 0:
            return (self.used_amount / self.coverage_amount) * 100
        return Decimal(0)
    
    def __repr__(self) -> str:
        return f"<Insurance(id={self.id}, policy='{self.policy_number}', provider='{self.provider_name}')>"