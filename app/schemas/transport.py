"""
Transport Schemas
"""

from pydantic import BaseModel, Field, validator, condecimal
from typing import Optional
from datetime import datetime
from decimal import Decimal


# Base Schema
class TransportBase(BaseModel):
    transport_number: str = Field(..., max_length=20, description="Unique transport number")
    ambulance_id: int = Field(..., gt=0)
    transport_type: str = Field(..., max_length=50)
    from_location: str = Field(..., max_length=200)
    to_location: str = Field(..., max_length=200)
    
    @validator('transport_type')
    def validate_transport_type(cls, v):
        valid = ['emergency', 'scheduled', 'inter_facility', 'discharge', 'admission', 'transfer']
        if v.lower() not in valid:
            raise ValueError(f"Transport type must be one of: {', '.join(valid)}")
        return v.lower()


# Create Schema
class TransportCreate(TransportBase):
    patient_id: Optional[int] = None
    
    from_address: Optional[str] = None
    to_address: Optional[str] = None
    
    distance_km: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    
    # Request Details
    request_date: str = Field(..., max_length=20)
    request_time: str = Field(..., max_length=10)
    requested_by: str = Field(..., max_length=200)
    
    # Scheduled Time
    scheduled_pickup_time: Optional[str] = Field(None, max_length=50)
    scheduled_dropoff_time: Optional[str] = Field(None, max_length=50)
    
    # Actual Times
    pickup_time: Optional[str] = Field(None, max_length=50)
    dropoff_time: Optional[str] = Field(None, max_length=50)
    departure_time: Optional[str] = Field(None, max_length=50)
    arrival_time: Optional[str] = Field(None, max_length=50)
    
    total_duration_minutes: Optional[int] = Field(None, ge=0)
    
    # Priority
    priority: str = Field(default='normal', max_length=20)
    
    # Patient Condition
    patient_condition: Optional[str] = None
    requires_oxygen: bool = Field(default=False)
    requires_ventilator: bool = Field(default=False)
    requires_stretcher: bool = Field(default=True)
    is_critical: bool = Field(default=False)
    
    # Staff
    driver_name: Optional[str] = Field(None, max_length=200)
    paramedic_name: Optional[str] = Field(None, max_length=200)
    nurse_name: Optional[str] = Field(None, max_length=200)
    doctor_name: Optional[str] = Field(None, max_length=200)
    
    # Contact
    contact_person: Optional[str] = Field(None, max_length=200)
    contact_phone: Optional[str] = Field(None, max_length=20)
    
    # Cost
    estimated_cost: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    actual_cost: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    
    # Status
    status: str = Field(default='requested', max_length=20)
    
    # Incident
    incident_reported: bool = Field(default=False)
    incident_description: Optional[str] = None
    
    # Vitals and Treatment
    vital_signs_recorded: Optional[str] = Field(None, description="JSON array")
    treatment_given: Optional[str] = None
    
    # Feedback
    service_rating: Optional[int] = Field(None, ge=1, le=5)
    feedback: Optional[str] = None
    
    # Notes
    special_instructions: Optional[str] = None
    notes: Optional[str] = None
    
    @validator('priority')
    def validate_priority(cls, v):
        valid = ['emergency', 'urgent', 'normal', 'scheduled']
        if v.lower() not in valid:
            raise ValueError(f"Priority must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validator('status')
    def validate_status(cls, v):
        valid = ['requested', 'assigned', 'dispatched', 'in_transit', 'completed', 'cancelled']
        if v.lower() not in valid:
            raise ValueError(f"Status must be one of: {', '.join(valid)}")
        return v.lower()


# Update Schema
class TransportUpdate(BaseModel):
    patient_id: Optional[int] = None
    
    scheduled_pickup_time: Optional[str] = Field(None, max_length=50)
    scheduled_dropoff_time: Optional[str] = Field(None, max_length=50)
    
    pickup_time: Optional[str] = Field(None, max_length=50)
    dropoff_time: Optional[str] = Field(None, max_length=50)
    departure_time: Optional[str] = Field(None, max_length=50)
    arrival_time: Optional[str] = Field(None, max_length=50)
    
    total_duration_minutes: Optional[int] = Field(None, ge=0)
    
    driver_name: Optional[str] = Field(None, max_length=200)
    paramedic_name: Optional[str] = Field(None, max_length=200)
    nurse_name: Optional[str] = Field(None, max_length=200)
    doctor_name: Optional[str] = Field(None, max_length=200)
    
    actual_cost: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    
    status: Optional[str] = Field(None, max_length=20)
    
    incident_reported: Optional[bool] = None
    incident_description: Optional[str] = None
    
    vital_signs_recorded: Optional[str] = None
    treatment_given: Optional[str] = None
    
    service_rating: Optional[int] = Field(None, ge=1, le=5)
    feedback: Optional[str] = None
    
    notes: Optional[str] = None


# Response Schema
class TransportResponse(TransportBase):
    id: int
    patient_id: Optional[int]
    
    from_address: Optional[str]
    to_address: Optional[str]
    
    distance_km: Optional[Decimal]
    
    request_date: str
    request_time: str
    requested_by: str
    
    scheduled_pickup_time: Optional[str]
    scheduled_dropoff_time: Optional[str]
    
    pickup_time: Optional[str]
    dropoff_time: Optional[str]
    departure_time: Optional[str]
    arrival_time: Optional[str]
    
    total_duration_minutes: Optional[int]
    
    priority: str
    
    patient_condition: Optional[str]
    requires_oxygen: bool
    requires_ventilator: bool
    requires_stretcher: bool
    is_critical: bool
    
    driver_name: Optional[str]
    paramedic_name: Optional[str]
    nurse_name: Optional[str]
    doctor_name: Optional[str]
    
    contact_person: Optional[str]
    contact_phone: Optional[str]
    
    estimated_cost: Optional[Decimal]
    actual_cost: Optional[Decimal]
    
    status: str
    
    incident_reported: bool
    incident_description: Optional[str]
    
    vital_signs_recorded: Optional[str]
    treatment_given: Optional[str]
    
    service_rating: Optional[int]
    feedback: Optional[str]
    
    special_instructions: Optional[str]
    notes: Optional[str]
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v)
        }


# List Response
class TransportListResponse(BaseModel):
    total: int
    items: list[TransportResponse]
    page: int
    page_size: int
    total_pages: int


# Transport Dispatch Schema
class TransportDispatchSchema(BaseModel):
    transport_id: int = Field(..., gt=0)
    ambulance_id: int = Field(..., gt=0)
    
    driver_name: str = Field(..., max_length=200)
    paramedic_name: Optional[str] = Field(None, max_length=200)
    
    dispatched_by: str = Field(..., max_length=200)
    dispatch_time: str = Field(..., max_length=50)
    
    estimated_arrival_time: str = Field(..., max_length=50)
    notes: Optional[str] = None


# Complete Transport Schema
class TransportCompleteSchema(BaseModel):
    pickup_time: str = Field(..., max_length=50)
    dropoff_time: str = Field(..., max_length=50)
    
    actual_cost: condecimal(max_digits=10, decimal_places=2, ge=0) = Field(...)
    
    distance_km: condecimal(max_digits=10, decimal_places=2, ge=0) = Field(...)
    
    treatment_given: Optional[str] = None
    vital_signs_recorded: Optional[str] = Field(None, description="JSON array")
    
    completed_by: str = Field(..., max_length=200)
    notes: Optional[str] = None