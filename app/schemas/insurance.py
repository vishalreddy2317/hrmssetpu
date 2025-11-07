"""
Insurance Schemas
Pydantic schemas for patient insurance and claims management
"""

from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict, EmailStr
from typing import Optional, List, Dict, Any, Union
from datetime import datetime, date, timedelta
from decimal import Decimal
from enum import Enum
import json
import re


# Enums
class PolicyType(str, Enum):
    """Insurance policy types"""
    INDIVIDUAL = "individual"
    FAMILY = "family"
    GROUP = "group"
    CORPORATE = "corporate"
    GOVERNMENT = "government"
    SENIOR_CITIZEN = "senior_citizen"
    STUDENT = "student"


class InsuranceStatus(str, Enum):
    """Insurance status"""
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    SUSPENDED = "suspended"
    PENDING_RENEWAL = "pending_renewal"
    PENDING_ACTIVATION = "pending_activation"


class NetworkType(str, Enum):
    """Network types"""
    PPO = "ppo"  # Preferred Provider Organization
    HMO = "hmo"  # Health Maintenance Organization
    EPO = "epo"  # Exclusive Provider Organization
    POS = "pos"  # Point of Service
    INDEMNITY = "indemnity"


class RelationToInsured(str, Enum):
    """Relationship to policy holder"""
    SELF = "self"
    SPOUSE = "spouse"
    CHILD = "child"
    PARENT = "parent"
    SIBLING = "sibling"
    DEPENDENT = "dependent"
    OTHER = "other"


class ClaimStatus(str, Enum):
    """Claim status"""
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    PARTIALLY_APPROVED = "partially_approved"
    PENDING_DOCUMENTS = "pending_documents"


# Helper Schemas
class PatientBasic(BaseModel):
    """Basic patient information"""
    id: int
    full_name: str
    patient_number: Optional[str] = None
    date_of_birth: Optional[str] = None
    phone: Optional[str] = None
    
    class Config:
        from_attributes = True


class PolicyHolderInfo(BaseModel):
    """Policy holder information"""
    policy_holder_name: str = Field(..., max_length=200, description="Policy holder name")
    policy_holder_relation: RelationToInsured = Field(..., description="Relation to patient")
    policy_holder_dob: Optional[str] = Field(None, description="Date of birth (YYYY-MM-DD)")
    policy_holder_id: Optional[str] = Field(None, description="ID/SSN number")
    policy_holder_phone: Optional[str] = Field(None, max_length=20)
    policy_holder_email: Optional[EmailStr] = None
    employer_name: Optional[str] = Field(None, description="Employer (for group/corporate)")
    
    @field_validator('policy_holder_dob')
    @classmethod
    def validate_dob(cls, v):
        if v is None:
            return None
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError("Date of birth must be in YYYY-MM-DD format")
    
    class Config:
        json_schema_extra = {
            "example": {
                "policy_holder_name": "John Doe Sr.",
                "policy_holder_relation": "parent",
                "policy_holder_dob": "1970-05-15",
                "policy_holder_phone": "+1-555-123-4567",
                "policy_holder_email": "john.sr@example.com"
            }
        }


class CoverageDetails(BaseModel):
    """Coverage type details"""
    inpatient_coverage: bool = Field(default=True, description="Inpatient coverage")
    outpatient_coverage: bool = Field(default=True, description="Outpatient coverage")
    emergency_coverage: bool = Field(default=True, description="Emergency coverage")
    maternity_coverage: bool = Field(default=False, description="Maternity coverage")
    dental_coverage: bool = Field(default=False, description="Dental coverage")
    vision_coverage: bool = Field(default=False, description="Vision coverage")
    prescription_coverage: bool = Field(default=True, description="Prescription drugs")
    mental_health_coverage: bool = Field(default=False, description="Mental health services")
    rehabilitation_coverage: bool = Field(default=False, description="Rehabilitation services")
    preventive_care_coverage: bool = Field(default=True, description="Preventive care")
    
    class Config:
        json_schema_extra = {
            "example": {
                "inpatient_coverage": True,
                "outpatient_coverage": True,
                "emergency_coverage": True,
                "maternity_coverage": True,
                "dental_coverage": False,
                "vision_coverage": False,
                "prescription_coverage": True,
                "mental_health_coverage": True,
                "rehabilitation_coverage": True,
                "preventive_care_coverage": True
            }
        }


class CopayInfo(BaseModel):
    """Co-payment information"""
    copay_percentage: Optional[Decimal] = Field(None, ge=0, le=100, description="Co-pay percentage")
    copay_amount: Optional[Decimal] = Field(None, ge=0, description="Fixed co-pay amount")
    copay_applies_to: Optional[List[str]] = Field(None, description="Services co-pay applies to")
    max_copay_annual: Optional[Decimal] = Field(None, ge=0, description="Maximum annual co-pay")
    
    class Config:
        json_schema_extra = {
            "example": {
                "copay_percentage": 20.0,
                "copay_amount": None,
                "copay_applies_to": ["outpatient", "specialist_visit"],
                "max_copay_annual": 5000.00
            }
        }


class DeductibleInfo(BaseModel):
    """Deductible information"""
    annual_deductible: Decimal = Field(..., ge=0, description="Annual deductible amount")
    deductible_met: Decimal = Field(default=Decimal('0.00'), ge=0, description="Amount met this year")
    deductible_remaining: Optional[Decimal] = Field(None, description="Remaining deductible")
    family_deductible: Optional[Decimal] = Field(None, ge=0, description="Family deductible (if applicable)")
    deductible_resets: Optional[str] = Field(None, description="When deductible resets")
    
    @model_validator(mode='after')
    def calculate_remaining(self):
        """Calculate remaining deductible"""
        if self.annual_deductible and self.deductible_met is not None:
            self.deductible_remaining = max(Decimal('0'), self.annual_deductible - self.deductible_met)
        return self
    
    class Config:
        json_schema_extra = {
            "example": {
                "annual_deductible": 2000.00,
                "deductible_met": 500.00,
                "deductible_remaining": 1500.00,
                "family_deductible": 4000.00,
                "deductible_resets": "January 1st annually"
            }
        }


class ProviderInfo(BaseModel):
    """Insurance provider information"""
    provider_name: str = Field(..., max_length=200, description="Provider name")
    provider_code: Optional[str] = Field(None, max_length=50, description="Provider code")
    provider_phone: Optional[str] = Field(None, max_length=20, description="Contact phone")
    provider_email: Optional[EmailStr] = Field(None, description="Contact email")
    provider_website: Optional[str] = Field(None, description="Provider website")
    customer_service_hours: Optional[str] = Field(None, description="Customer service hours")
    claims_address: Optional[str] = Field(None, description="Claims submission address")
    
    @field_validator('provider_phone')
    @classmethod
    def validate_phone(cls, v):
        if v is None:
            return None
        cleaned = re.sub(r'[\s\-\(\)]', '', v)
        if not re.match(r'^\+?[0-9]{10,15}$', cleaned):
            raise ValueError("Invalid phone number format")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "provider_name": "Blue Cross Blue Shield",
                "provider_code": "BCBS",
                "provider_phone": "1-800-555-1234",
                "provider_email": "claims@bcbs.com",
                "provider_website": "www.bcbs.com",
                "customer_service_hours": "Mon-Fri 8AM-8PM EST"
            }
        }


class PreExistingConditions(BaseModel):
    """Pre-existing conditions coverage"""
    pre_existing_covered: bool = Field(..., description="Pre-existing conditions covered")
    waiting_period_months: Optional[int] = Field(None, ge=0, le=120, description="Waiting period in months")
    conditions_list: Optional[List[str]] = Field(None, description="List of covered conditions")
    exclusions: Optional[List[str]] = Field(None, description="Excluded conditions")
    
    class Config:
        json_schema_extra = {
            "example": {
                "pre_existing_covered": True,
                "waiting_period_months": 12,
                "conditions_list": ["Diabetes", "Hypertension"],
                "exclusions": ["Cosmetic procedures"]
            }
        }


class NetworkInfo(BaseModel):
    """Network information"""
    network_type: NetworkType = Field(..., description="Type of network")
    is_network_hospital: bool = Field(..., description="Is this hospital in network")
    network_name: Optional[str] = Field(None, description="Network name")
    out_of_network_coverage: bool = Field(default=False, description="Coverage for out-of-network")
    out_of_network_copay: Optional[Decimal] = Field(None, description="Higher co-pay for out-of-network")
    
    class Config:
        json_schema_extra = {
            "example": {
                "network_type": "ppo",
                "is_network_hospital": True,
                "network_name": "Premier Care Network",
                "out_of_network_coverage": True,
                "out_of_network_copay": 40.0
            }
        }


class ClaimSummary(BaseModel):
    """Claim statistics summary"""
    total_claims: int = Field(default=0, ge=0)
    approved_claims: int = Field(default=0, ge=0)
    rejected_claims: int = Field(default=0, ge=0)
    pending_claims: int = Field(default=0, ge=0)
    total_claimed_amount: Decimal = Field(default=Decimal('0.00'), ge=0)
    total_approved_amount: Decimal = Field(default=Decimal('0.00'), ge=0)
    approval_rate: Optional[float] = Field(None, description="Approval rate percentage")
    
    @model_validator(mode='after')
    def calculate_approval_rate(self):
        """Calculate claim approval rate"""
        if self.total_claims > 0:
            self.approval_rate = round((self.approved_claims / self.total_claims) * 100, 2)
        return self
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_claims": 25,
                "approved_claims": 22,
                "rejected_claims": 2,
                "pending_claims": 1,
                "total_claimed_amount": 50000.00,
                "total_approved_amount": 45000.00,
                "approval_rate": 88.0
            }
        }


# Base Schema
class InsuranceBase(BaseModel):
    """Base schema for insurance"""
    insurance_number: str = Field(..., max_length=50, description="Unique insurance identifier")
    policy_number: str = Field(..., max_length=100, description="Insurance policy number")
    
    # Patient
    patient_id: int = Field(..., description="Patient ID")
    
    # Provider
    provider_name: str = Field(..., max_length=200, description="Insurance provider")
    provider_code: Optional[str] = Field(None, max_length=50)
    provider_phone: Optional[str] = Field(None, max_length=20)
    provider_email: Optional[EmailStr] = None
    
    # Policy Details
    policy_type: PolicyType = Field(..., description="Type of policy")
    plan_name: str = Field(..., max_length=200, description="Plan/product name")
    
    # Coverage
    coverage_amount: Decimal = Field(..., gt=0, decimal_places=2, description="Total coverage amount")
    used_amount: Decimal = Field(default=Decimal('0.00'), ge=0, decimal_places=2, description="Amount used")
    remaining_amount: Decimal = Field(..., ge=0, decimal_places=2, description="Remaining coverage")
    
    # Validity
    start_date: str = Field(..., description="Policy start date (YYYY-MM-DD)")
    end_date: str = Field(..., description="Policy end date (YYYY-MM-DD)")
    is_active: bool = Field(default=True, description="Active status")
    
    # Policy Holder
    policy_holder_name: str = Field(..., max_length=200)
    policy_holder_relation: Optional[str] = Field(None, max_length=50)
    policy_holder_dob: Optional[str] = Field(None)
    
    # Co-payment
    copay_percentage: Optional[Decimal] = Field(None, ge=0, le=100)
    copay_amount: Optional[Decimal] = Field(None, ge=0)
    
    # Deductible
    annual_deductible: Optional[Decimal] = Field(None, ge=0)
    deductible_met: Decimal = Field(default=Decimal('0.00'), ge=0)
    
    # Coverage Types
    inpatient_coverage: bool = Field(default=True)
    outpatient_coverage: bool = Field(default=True)
    emergency_coverage: bool = Field(default=True)
    maternity_coverage: bool = Field(default=False)
    dental_coverage: bool = Field(default=False)
    vision_coverage: bool = Field(default=False)
    
    # Pre-existing
    pre_existing_covered: bool = Field(default=False)
    waiting_period_months: Optional[int] = Field(None, ge=0)
    
    # Network
    network_type: Optional[NetworkType] = None
    is_network_hospital: bool = Field(default=True)
    
    # Claims
    total_claims: int = Field(default=0, ge=0)
    approved_claims: int = Field(default=0, ge=0)
    rejected_claims: int = Field(default=0, ge=0)
    
    # Status
    status: InsuranceStatus = Field(default=InsuranceStatus.ACTIVE)
    
    # Documents
    policy_document_url: Optional[str] = Field(None, max_length=500)
    id_card_url: Optional[str] = Field(None, max_length=500)
    
    # Notes
    notes: Optional[str] = None
    exclusions: Optional[str] = None

    @field_validator('start_date', 'end_date', 'policy_holder_dob')
    @classmethod
    def validate_date_format(cls, v):
        """Validate date format"""
        if v is None:
            return None
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
    
    @field_validator('provider_phone')
    @classmethod
    def validate_phone(cls, v):
        if v is None:
            return None
        cleaned = re.sub(r'[\s\-\(\)]', '', v)
        if not re.match(r'^\+?[0-9]{10,15}$', cleaned):
            raise ValueError("Invalid phone number format")
        return v
    
    @model_validator(mode='after')
    def validate_dates(self):
        """Validate date ranges"""
        if self.start_date and self.end_date:
            start = datetime.strptime(self.start_date, '%Y-%m-%d')
            end = datetime.strptime(self.end_date, '%Y-%m-%d')
            if end <= start:
                raise ValueError("End date must be after start date")
        return self
    
    @model_validator(mode='after')
    def validate_coverage_amounts(self):
        """Validate coverage amounts consistency"""
        if self.used_amount > self.coverage_amount:
            raise ValueError("Used amount cannot exceed coverage amount")
        
        expected_remaining = self.coverage_amount - self.used_amount
        if abs(self.remaining_amount - expected_remaining) > Decimal('0.01'):
            # Auto-correct remaining amount
            self.remaining_amount = expected_remaining
        
        return self


# Create Schema
class InsuranceCreate(BaseModel):
    """Schema for creating insurance policy"""
    policy_number: str = Field(..., max_length=100)
    patient_id: int
    
    # Provider (use nested schema or flat)
    provider: ProviderInfo = Field(..., description="Provider information")
    
    # Policy
    policy_type: PolicyType
    plan_name: str = Field(..., max_length=200)
    
    # Coverage
    coverage_amount: Decimal = Field(..., gt=0, decimal_places=2)
    
    # Validity
    start_date: str = Field(..., description="YYYY-MM-DD")
    end_date: str = Field(..., description="YYYY-MM-DD")
    
    # Policy Holder
    policy_holder: PolicyHolderInfo = Field(..., description="Policy holder details")
    
    # Financial
    copay_info: Optional[CopayInfo] = None
    deductible_info: Optional[DeductibleInfo] = None
    
    # Coverage types
    coverage_details: CoverageDetails = Field(default_factory=CoverageDetails)
    
    # Pre-existing
    pre_existing: Optional[PreExistingConditions] = None
    
    # Network
    network_info: NetworkInfo = Field(..., description="Network information")
    
    # Documents
    policy_document_url: Optional[str] = None
    id_card_url: Optional[str] = None
    
    # Notes
    notes: Optional[str] = None
    exclusions: Optional[str] = None
    
    # Auto-generated
    insurance_number: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "policy_number": "POL-123456789",
                "patient_id": 123,
                "provider": {
                    "provider_name": "Blue Cross Blue Shield",
                    "provider_code": "BCBS",
                    "provider_phone": "1-800-555-1234",
                    "provider_email": "claims@bcbs.com"
                },
                "policy_type": "family",
                "plan_name": "Gold PPO Plan",
                "coverage_amount": 500000.00,
                "start_date": "2024-01-01",
                "end_date": "2024-12-31",
                "policy_holder": {
                    "policy_holder_name": "John Doe",
                    "policy_holder_relation": "self",
                    "policy_holder_dob": "1980-05-15"
                },
                "network_info": {
                    "network_type": "ppo",
                    "is_network_hospital": True
                }
            }
        }


# Update Schema
class InsuranceUpdate(BaseModel):
    """Schema for updating insurance"""
    provider_phone: Optional[str] = None
    provider_email: Optional[EmailStr] = None
    plan_name: Optional[str] = None
    coverage_amount: Optional[Decimal] = Field(None, gt=0)
    used_amount: Optional[Decimal] = Field(None, ge=0)
    remaining_amount: Optional[Decimal] = Field(None, ge=0)
    end_date: Optional[str] = None
    is_active: Optional[bool] = None
    copay_percentage: Optional[Decimal] = Field(None, ge=0, le=100)
    copay_amount: Optional[Decimal] = Field(None, ge=0)
    deductible_met: Optional[Decimal] = Field(None, ge=0)
    status: Optional[InsuranceStatus] = None
    policy_document_url: Optional[str] = None
    id_card_url: Optional[str] = None
    notes: Optional[str] = None


# Response Schema
class InsuranceResponse(InsuranceBase):
    """Schema for insurance response"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    # Calculated fields
    days_until_expiry: Optional[int] = Field(None, description="Days until policy expires")
    is_expiring_soon: bool = Field(default=False, description="Expires within 30 days")
    is_expired: bool = Field(default=False, description="Policy has expired")
    utilization_percentage: float = Field(..., description="Coverage utilization %")
    remaining_percentage: float = Field(..., description="Remaining coverage %")
    deductible_remaining: Optional[Decimal] = Field(None, description="Remaining deductible")
    approval_rate: Optional[float] = Field(None, description="Claim approval rate %")
    
    model_config = ConfigDict(from_attributes=True)
    
    @model_validator(mode='after')
    def calculate_fields(self):
        """Calculate additional fields"""
        # Expiry calculations
        if self.end_date:
            end_dt = datetime.strptime(self.end_date, '%Y-%m-%d')
            today = datetime.now()
            delta = (end_dt.date() - today.date()).days
            self.days_until_expiry = delta
            self.is_expired = delta < 0
            self.is_expiring_soon = 0 <= delta <= 30
        
        # Utilization
        if self.coverage_amount > 0:
            self.utilization_percentage = round(float((self.used_amount / self.coverage_amount) * 100), 2)
            self.remaining_percentage = round(float((self.remaining_amount / self.coverage_amount) * 100), 2)
        else:
            self.utilization_percentage = 0.0
            self.remaining_percentage = 0.0
        
        # Deductible
        if self.annual_deductible:
            self.deductible_remaining = max(Decimal('0'), self.annual_deductible - self.deductible_met)
        
        # Approval rate
        if self.total_claims > 0:
            self.approval_rate = round((self.approved_claims / self.total_claims) * 100, 2)
        
        return self
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "insurance_number": "INS-2024-0001",
                "policy_number": "POL-123456789",
                "patient_id": 123,
                "provider_name": "Blue Cross Blue Shield",
                "policy_type": "family",
                "plan_name": "Gold PPO Plan",
                "coverage_amount": 500000.00,
                "used_amount": 50000.00,
                "remaining_amount": 450000.00,
                "utilization_percentage": 10.0,
                "remaining_percentage": 90.0,
                "start_date": "2024-01-01",
                "end_date": "2024-12-31",
                "status": "active",
                "is_expired": False,
                "is_expiring_soon": False,
                "days_until_expiry": 300,
                "created_at": "2024-01-01T10:00:00",
                "updated_at": "2024-01-15T10:00:00"
            }
        }


# Detail Response with Relationships
class InsuranceDetailResponse(InsuranceResponse):
    """Detailed insurance with relationships"""
    patient: Optional[PatientBasic] = None
    
    # Enhanced details
    provider_info: Optional[ProviderInfo] = None
    policy_holder_info: Optional[PolicyHolderInfo] = None
    coverage_breakdown: Optional[CoverageDetails] = None
    copay_details: Optional[CopayInfo] = None
    deductible_details: Optional[DeductibleInfo] = None
    network_details: Optional[NetworkInfo] = None
    claim_summary: Optional[ClaimSummary] = None
    
    model_config = ConfigDict(from_attributes=True)


# List Response Schema
class InsuranceListResponse(BaseModel):
    """Schema for paginated list of insurance policies"""
    total: int = Field(..., description="Total number of records")
    page: int = Field(..., ge=1, description="Current page number")
    page_size: int = Field(..., ge=1, le=100, description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")
    items: List[InsuranceResponse] = Field(..., description="Insurance items")
    summary: Optional[Dict[str, Any]] = Field(None, description="Summary statistics")


# Filter Schema
class InsuranceFilter(BaseModel):
    """Schema for filtering insurance policies"""
    # ID filters
    patient_id: Optional[int] = Field(None, description="Filter by patient ID")
    
    # String filters
    insurance_number: Optional[str] = Field(None, description="Filter by insurance number")
    policy_number: Optional[str] = Field(None, description="Filter by policy number")
    provider_name: Optional[str] = Field(None, description="Filter by provider")
    policy_holder_name: Optional[str] = Field(None, description="Filter by policy holder")
    
    # Type filters
    policy_type: Optional[Union[PolicyType, List[PolicyType]]] = Field(None, description="Filter by policy type")
    status: Optional[Union[InsuranceStatus, List[InsuranceStatus]]] = Field(None, description="Filter by status")
    network_type: Optional[NetworkType] = Field(None, description="Filter by network type")
    
    # Boolean filters
    is_active: Optional[bool] = Field(None, description="Active policies only")
    is_network_hospital: Optional[bool] = Field(None, description="In-network only")
    pre_existing_covered: Optional[bool] = Field(None, description="Pre-existing covered")
    expiring_soon: Optional[bool] = Field(None, description="Expiring within 30 days")
    expired: Optional[bool] = Field(None, description="Expired policies")
    
    # Coverage filters
    min_coverage: Optional[Decimal] = Field(None, ge=0, description="Minimum coverage amount")
    max_coverage: Optional[Decimal] = Field(None, ge=0, description="Maximum coverage amount")
    high_utilization: Optional[bool] = Field(None, description="Utilization > 80%")
    
    # Date filters
    start_date_from: Optional[str] = Field(None, description="Start date from")
    start_date_to: Optional[str] = Field(None, description="Start date to")
    end_date_from: Optional[str] = Field(None, description="End date from")
    end_date_to: Optional[str] = Field(None, description="End date to")
    
    # Coverage type filters
    has_maternity: Optional[bool] = Field(None, description="Has maternity coverage")
    has_dental: Optional[bool] = Field(None, description="Has dental coverage")
    has_vision: Optional[bool] = Field(None, description="Has vision coverage")
    
    # Search
    search: Optional[str] = Field(None, description="Search in policy number, provider, plan name")
    
    # Pagination
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")
    
    # Sorting
    sort_by: str = Field("end_date", description="Field to sort by")
    sort_order: str = Field("asc", pattern="^(asc|desc)$", description="Sort order")
    
    # Include relationships
    include_patient: bool = Field(False, description="Include patient details")
    include_claims: bool = Field(False, description="Include claim summary")

    @field_validator('start_date_from', 'start_date_to', 'end_date_from', 'end_date_to')
    @classmethod
    def validate_date(cls, v):
        if v is None:
            return None
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")


# Eligibility Check Schema
class EligibilityCheck(BaseModel):
    """Schema for insurance eligibility verification"""
    insurance_id: int = Field(..., description="Insurance ID")
    service_type: str = Field(..., description="Type of service")
    service_code: Optional[str] = Field(None, description="CPT/procedure code")
    estimated_cost: Decimal = Field(..., gt=0, description="Estimated service cost")
    service_date: Optional[str] = Field(None, description="Planned service date")
    
    class Config:
        json_schema_extra = {
            "example": {
                "insurance_id": 1,
                "service_type": "inpatient_surgery",
                "service_code": "CPT-12345",
                "estimated_cost": 15000.00,
                "service_date": "2024-02-01"
            }
        }


class EligibilityResponse(BaseModel):
    """Eligibility check response"""
    is_eligible: bool = Field(..., description="Service is covered")
    coverage_percentage: Optional[Decimal] = Field(None, description="Coverage %")
    patient_responsibility: Optional[Decimal] = Field(None, description="Patient pays")
    insurance_pays: Optional[Decimal] = Field(None, description="Insurance pays")
    requires_preauth: bool = Field(default=False, description="Pre-authorization required")
    deductible_applies: bool = Field(default=False, description="Deductible applies")
    copay_amount: Optional[Decimal] = Field(None, description="Co-pay amount")
    remaining_coverage: Decimal = Field(..., description="Remaining coverage")
    denial_reason: Optional[str] = Field(None, description="Reason if not eligible")
    notes: Optional[str] = Field(None, description="Additional notes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "is_eligible": True,
                "coverage_percentage": 80.0,
                "patient_responsibility": 3000.00,
                "insurance_pays": 12000.00,
                "requires_preauth": True,
                "deductible_applies": False,
                "copay_amount": 500.00,
                "remaining_coverage": 438000.00,
                "notes": "Pre-authorization required within 48 hours of admission"
            }
        }


# Pre-Authorization Schema
class PreAuthorizationRequest(BaseModel):
    """Pre-authorization request"""
    insurance_id: int
    patient_id: int
    procedure_code: str = Field(..., description="CPT/procedure code")
    procedure_name: str = Field(..., description="Procedure name")
    diagnosis_code: str = Field(..., description="ICD diagnosis code")
    diagnosis_description: str = Field(..., description="Diagnosis")
    requesting_doctor_id: int
    facility_name: str = Field(..., description="Where procedure will be performed")
    estimated_cost: Decimal = Field(..., gt=0)
    planned_date: str = Field(..., description="Planned date (YYYY-MM-DD)")
    urgency: str = Field(default="routine", pattern="^(stat|urgent|routine)$")
    clinical_justification: str = Field(..., min_length=50, description="Medical necessity justification")
    supporting_documents: Optional[List[str]] = Field(None, description="Document URLs")
    
    class Config:
        json_schema_extra = {
            "example": {
                "insurance_id": 1,
                "patient_id": 123,
                "procedure_code": "CPT-47562",
                "procedure_name": "Laparoscopic Cholecystectomy",
                "diagnosis_code": "K80.20",
                "diagnosis_description": "Calculus of gallbladder without cholecystitis",
                "requesting_doctor_id": 45,
                "facility_name": "Central Hospital - Surgical Wing",
                "estimated_cost": 18000.00,
                "planned_date": "2024-02-15",
                "urgency": "urgent",
                "clinical_justification": "Patient has recurrent gallstone attacks. Conservative management has failed..."
            }
        }


class PreAuthorizationResponse(BaseModel):
    """Pre-authorization response"""
    auth_number: str = Field(..., description="Authorization number")
    status: str = Field(..., pattern="^(approved|denied|pending)$")
    approved_amount: Optional[Decimal] = None
    valid_from: Optional[str] = None
    valid_until: Optional[str] = None
    conditions: Optional[List[str]] = Field(None, description="Conditions for approval")
    denial_reason: Optional[str] = None
    appeal_process: Optional[str] = None
    reviewer_notes: Optional[str] = None
    reviewed_by: Optional[str] = None
    review_date: Optional[datetime] = None


# Claim Submission Schema
class ClaimSubmission(BaseModel):
    """Insurance claim submission"""
    insurance_id: int
    patient_id: int
    claim_number: Optional[str] = None  # Auto-generated
    
    # Service details
    service_date: str = Field(..., description="Service date (YYYY-MM-DD)")
    admission_id: Optional[int] = Field(None, description="Admission ID if inpatient")
    
    # Charges
    total_charges: Decimal = Field(..., gt=0, description="Total billed amount")
    itemized_charges: List[Dict[str, Any]] = Field(..., description="Itemized bill")
    
    # Codes
    diagnosis_codes: List[str] = Field(..., min_length=1, description="ICD diagnosis codes")
    procedure_codes: List[str] = Field(..., min_length=1, description="CPT procedure codes")
    
    # Provider
    treating_doctor_id: int
    billing_department: str
    
    # Documents
    supporting_documents: List[str] = Field(..., min_length=1, description="Bill, reports, prescriptions")
    
    # Pre-auth (if applicable)
    preauth_number: Optional[str] = None
    
    # Notes
    claim_notes: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "insurance_id": 1,
                "patient_id": 123,
                "service_date": "2024-01-15",
                "admission_id": 456,
                "total_charges": 25000.00,
                "itemized_charges": [
                    {"item": "Room Charges", "amount": 5000.00},
                    {"item": "Surgery", "amount": 15000.00},
                    {"item": "Medications", "amount": 3000.00},
                    {"item": "Lab Tests", "amount": 2000.00}
                ],
                "diagnosis_codes": ["K80.20"],
                "procedure_codes": ["CPT-47562"],
                "treating_doctor_id": 45,
                "billing_department": "Finance",
                "supporting_documents": [
                    "invoice_123.pdf",
                    "discharge_summary.pdf"
                ],
                "preauth_number": "AUTH-2024-001"
            }
        }


class ClaimResponse(BaseModel):
    """Claim submission response"""
    claim_id: int
    claim_number: str
    status: ClaimStatus
    submitted_date: datetime
    claimed_amount: Decimal
    approved_amount: Optional[Decimal] = None
    rejected_amount: Optional[Decimal] = None
    patient_responsibility: Optional[Decimal] = None
    processing_time_days: Optional[int] = None
    reviewer_notes: Optional[str] = None
    payment_status: Optional[str] = None
    payment_date: Optional[str] = None


# Renew Policy Schema
class RenewInsurance(BaseModel):
    """Renew insurance policy"""
    new_end_date: str = Field(..., description="New end date (YYYY-MM-DD)")
    new_coverage_amount: Optional[Decimal] = Field(None, gt=0, description="Updated coverage")
    new_plan_name: Optional[str] = Field(None, description="Plan change")
    premium_amount: Decimal = Field(..., gt=0, description="Renewal premium")
    payment_method: str = Field(..., description="Payment method")
    reset_deductible: bool = Field(default=True, description="Reset annual deductible")
    
    @field_validator('new_end_date')
    @classmethod
    def validate_date(cls, v):
        try:
            new_end = datetime.strptime(v, '%Y-%m-%d')
            if new_end.date() <= datetime.now().date():
                raise ValueError("New end date must be in the future")
            return v
        except ValueError as e:
            if "does not match format" in str(e):
                raise ValueError("Date must be in YYYY-MM-DD format")
            raise


# Statistics Schema
class InsuranceStats(BaseModel):
    """Insurance statistics"""
    total_policies: int
    active_policies: int
    expired_policies: int
    expiring_soon: int
    
    # By type
    policies_by_type: Dict[str, int]
    policies_by_provider: Dict[str, int]
    policies_by_status: Dict[str, int]
    
    # Financial
    total_coverage: Decimal
    total_used: Decimal
    total_remaining: Decimal
    average_utilization: float
    
    # Claims
    total_claims_submitted: int
    total_claims_approved: int
    total_claims_rejected: int
    overall_approval_rate: float
    
    # Network
    in_network_count: int
    out_of_network_count: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_policies": 500,
                "active_policies": 450,
                "expired_policies": 40,
                "expiring_soon": 25,
                "policies_by_type": {
                    "individual": 200,
                    "family": 180,
                    "corporate": 120
                },
                "policies_by_provider": {
                    "Blue Cross": 200,
                    "Aetna": 150,
                    "Cigna": 150
                },
                "policies_by_status": {
                    "active": 450,
                    "expired": 40,
                    "suspended": 10
                },
                "total_coverage": 250000000.00,
                "total_used": 50000000.00,
                "total_remaining": 200000000.00,
                "average_utilization": 20.0,
                "total_claims_submitted": 2500,
                "total_claims_approved": 2200,
                "total_claims_rejected": 250,
                "overall_approval_rate": 88.0,
                "in_network_count": 400,
                "out_of_network_count": 100
            }
        }


# Export Schema
class InsuranceExport(BaseModel):
    """Export insurance data"""
    filters: InsuranceFilter
    export_format: str = Field(..., pattern="^(csv|xlsx|pdf|json)$")
    include_claims: bool = Field(default=False)
    include_documents: bool = Field(default=False)
    anonymize: bool = Field(default=False)


# Bulk Operations
class InsuranceBulkStatusUpdate(BaseModel):
    """Bulk update insurance status"""
    insurance_ids: List[int] = Field(..., min_length=1, max_length=50)
    status: InsuranceStatus
    reason: Optional[str] = None
    
    @field_validator('insurance_ids')
    @classmethod
    def validate_ids(cls, v):
        if len(v) > 50:
            raise ValueError("Cannot update more than 50 policies at once")
        return v