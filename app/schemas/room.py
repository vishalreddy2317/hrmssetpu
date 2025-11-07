"""
Room Schemas
"""

from pydantic import BaseModel, Field, validator, condecimal
from typing import Optional
from datetime import datetime
from decimal import Decimal


# Base Schema
class RoomBase(BaseModel):
    room_number: str = Field(..., max_length=20, description="Unique room number")
    room_name: Optional[str] = Field(None, max_length=100)
    room_type: str = Field(..., max_length=50)
    
    @validator('room_type')
    def validate_room_type(cls, v):
        valid = [
            'general', 'private', 'semi_private', 'icu', 'operation',
            'emergency', 'consultation', 'observation', 'isolation',
            'labor', 'recovery', 'nicu', 'pediatric'
        ]
        if v.lower() not in valid:
            raise ValueError(f"Room type must be one of: {', '.join(valid)}")
        return v.lower()


# Create Schema
class RoomCreate(RoomBase):
    # Floor Reference - NEW
    floor_id: Optional[int] = None
    floor_number: Optional[int] = Field(None, description="Floor number (0=Ground, -1=Basement 1)")
    
    # Location
    ward_id: Optional[int] = None
    department_id: Optional[int] = None
    building: Optional[str] = Field(None, max_length=50)
    wing: Optional[str] = Field(None, max_length=50)
    
    # Capacity
    bed_capacity: int = Field(default=1, ge=1)
    current_occupancy: int = Field(default=0, ge=0)
    
    # Room Specifications
    size_sqft: Optional[condecimal(max_digits=10, decimal_places=2, gt=0)] = None
    has_attached_bathroom: bool = Field(default=False)
    has_ac: bool = Field(default=False)
    has_window: bool = Field(default=True)
    has_balcony: bool = Field(default=False)
    has_tv: bool = Field(default=False)
    has_telephone: bool = Field(default=False)
    has_refrigerator: bool = Field(default=False)
    
    # Medical Equipment
    has_oxygen_supply: bool = Field(default=False)
    has_suction: bool = Field(default=False)
    has_monitor: bool = Field(default=False)
    has_ventilator: bool = Field(default=False)
    
    # Availability
    status: str = Field(default='available', max_length=20)
    is_available: bool = Field(default=True)
    is_isolation_room: bool = Field(default=False)
    
    # Pricing
    price_per_day: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    deposit_amount: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    
    # Additional Info
    description: Optional[str] = None
    special_equipment: Optional[str] = None
    notes: Optional[str] = None
    
    # Housekeeping
    last_cleaned_at: Optional[str] = Field(None, max_length=50)
    last_maintenance_at: Optional[str] = Field(None, max_length=50)
    
    @validator('status')
    def validate_status(cls, v):
        valid = [
            'available', 'occupied', 'maintenance', 'reserved',
            'cleaning', 'under_renovation', 'quarantine'
        ]
        if v.lower() not in valid:
            raise ValueError(f"Status must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validator('current_occupancy')
    def validate_occupancy(cls, v, values):
        if 'bed_capacity' in values and v > values['bed_capacity']:
            raise ValueError("Current occupancy cannot exceed bed capacity")
        return v


# Update Schema
class RoomUpdate(BaseModel):
    room_name: Optional[str] = Field(None, max_length=100)
    room_type: Optional[str] = Field(None, max_length=50)
    
    floor_id: Optional[int] = None
    floor_number: Optional[int] = None
    
    ward_id: Optional[int] = None
    department_id: Optional[int] = None
    building: Optional[str] = Field(None, max_length=50)
    wing: Optional[str] = Field(None, max_length=50)
    
    bed_capacity: Optional[int] = Field(None, ge=1)
    current_occupancy: Optional[int] = Field(None, ge=0)
    
    size_sqft: Optional[condecimal(max_digits=10, decimal_places=2, gt=0)] = None
    has_attached_bathroom: Optional[bool] = None
    has_ac: Optional[bool] = None
    has_window: Optional[bool] = None
    has_balcony: Optional[bool] = None
    has_tv: Optional[bool] = None
    has_telephone: Optional[bool] = None
    has_refrigerator: Optional[bool] = None
    
    has_oxygen_supply: Optional[bool] = None
    has_suction: Optional[bool] = None
    has_monitor: Optional[bool] = None
    has_ventilator: Optional[bool] = None
    
    status: Optional[str] = Field(None, max_length=20)
    is_available: Optional[bool] = None
    is_isolation_room: Optional[bool] = None
    
    price_per_day: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    deposit_amount: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    
    description: Optional[str] = None
    special_equipment: Optional[str] = None
    notes: Optional[str] = None
    
    last_cleaned_at: Optional[str] = Field(None, max_length=50)
    last_maintenance_at: Optional[str] = Field(None, max_length=50)


# Response Schema
class RoomResponse(RoomBase):
    id: int
    
    # Floor Reference
    floor_id: Optional[int]
    floor_number: Optional[int]
    floor_display: str
    
    # Location
    ward_id: Optional[int]
    department_id: Optional[int]
    building: Optional[str]
    wing: Optional[str]
    
    # Capacity
    bed_capacity: int
    current_occupancy: int
    available_beds: int
    is_full: bool
    occupancy_rate: float
    
    # Room Specifications
    size_sqft: Optional[Decimal]
    has_attached_bathroom: bool
    has_ac: bool
    has_window: bool
    has_balcony: bool
    has_tv: bool
    has_telephone: bool
    has_refrigerator: bool
    
    # Medical Equipment
    has_oxygen_supply: bool
    has_suction: bool
    has_monitor: bool
    has_ventilator: bool
    
    # Availability
    status: str
    is_available: bool
    is_isolation_room: bool
    
    # Pricing
    price_per_day: Optional[Decimal]
    deposit_amount: Optional[Decimal]
    
    # Additional Info
    description: Optional[str]
    special_equipment: Optional[str]
    notes: Optional[str]
    
    # Housekeeping
    last_cleaned_at: Optional[str]
    last_maintenance_at: Optional[str]
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v)
        }


# List Response
class RoomListResponse(BaseModel):
    total: int
    available_rooms: int
    occupied_rooms: int
    items: list[RoomResponse]
    page: int
    page_size: int
    total_pages: int


# Room Summary Schema
class RoomSummarySchema(BaseModel):
    total_rooms: int
    available_rooms: int
    occupied_rooms: int
    under_maintenance: int
    reserved_rooms: int
    
    # By Type
    rooms_by_type: dict  # {type: count}
    
    # By Floor
    rooms_by_floor: dict  # {floor_number: count}
    
    # By Department
    rooms_by_department: dict  # {department_id: count}
    
    # Occupancy
    total_capacity: int
    total_occupied: int
    average_occupancy_rate: float
    
    # ICU Specific
    icu_total: int
    icu_available: int
    icu_occupied: int
    
    # Isolation Specific
    isolation_total: int
    isolation_available: int
    isolation_occupied: int


# Room Filter Schema
class RoomFilterSchema(BaseModel):
    room_type: Optional[str] = Field(None, max_length=50)
    floor_id: Optional[int] = None
    floor_number: Optional[int] = None
    ward_id: Optional[int] = None
    department_id: Optional[int] = None
    building: Optional[str] = Field(None, max_length=50)
    wing: Optional[str] = Field(None, max_length=50)
    
    status: Optional[str] = Field(None, max_length=20)
    is_available: Optional[bool] = None
    is_isolation_room: Optional[bool] = None
    
    has_attached_bathroom: Optional[bool] = None
    has_ac: Optional[bool] = None
    has_oxygen_supply: Optional[bool] = None
    has_ventilator: Optional[bool] = None
    
    min_capacity: Optional[int] = Field(None, ge=1)
    max_capacity: Optional[int] = Field(None, ge=1)
    
    min_price: Optional[Decimal] = None
    max_price: Optional[Decimal] = None
    
    min_size: Optional[Decimal] = None
    max_size: Optional[Decimal] = None


# Room Availability Search Schema
class RoomAvailabilitySearchSchema(BaseModel):
    room_type: Optional[str] = Field(None, max_length=50)
    floor_number: Optional[int] = None
    ward_id: Optional[int] = None
    department_id: Optional[int] = None
    
    min_beds_required: int = Field(default=1, ge=1)
    
    # Required Facilities
    require_attached_bathroom: bool = Field(default=False)
    require_ac: bool = Field(default=False)
    require_oxygen_supply: bool = Field(default=False)
    require_ventilator: bool = Field(default=False)
    require_monitor: bool = Field(default=False)
    
    # For isolation cases
    isolation_required: bool = Field(default=False)
    
    # Budget
    max_price_per_day: Optional[Decimal] = None


# Room Availability Response
class RoomAvailabilityResponse(BaseModel):
    room_id: int
    room_number: str
    room_name: Optional[str]
    room_type: str
    floor_number: Optional[int]
    floor_display: str
    
    available_beds: int
    bed_capacity: int
    price_per_day: Optional[Decimal]
    
    # Facilities
    has_attached_bathroom: bool
    has_ac: bool
    has_oxygen_supply: bool
    has_ventilator: bool
    has_monitor: bool
    
    ward_id: Optional[int]
    department_id: Optional[int]
    building: Optional[str]
    wing: Optional[str]
    
    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }


# Room Assignment Schema
class RoomAssignmentSchema(BaseModel):
    patient_id: int = Field(..., gt=0)
    admission_id: Optional[int] = None
    bed_id: Optional[int] = None
    
    assigned_by: str = Field(..., max_length=200)
    assignment_date: str = Field(..., max_length=20)
    assignment_time: str = Field(..., max_length=10)
    
    expected_duration_days: Optional[int] = Field(None, gt=0)
    notes: Optional[str] = None


# Room Transfer Schema
class RoomTransferSchema(BaseModel):
    patient_id: int = Field(..., gt=0)
    from_room_id: int = Field(..., gt=0)
    to_room_id: int = Field(..., gt=0)
    
    from_bed_id: Optional[int] = None
    to_bed_id: Optional[int] = None
    
    transfer_reason: str = Field(..., description="Reason for room transfer")
    transferred_by: str = Field(..., max_length=200)
    transfer_date: str = Field(..., max_length=20)
    transfer_time: str = Field(..., max_length=10)
    
    notes: Optional[str] = None


# Room Cleaning Schema
class RoomCleaningSchema(BaseModel):
    cleaned_by: str = Field(..., max_length=200)
    cleaning_date: str = Field(..., max_length=20)
    cleaning_time: str = Field(..., max_length=10)
    
    cleaning_type: str = Field(..., max_length=50, description="routine, deep, terminal, discharge")
    
    areas_cleaned: Optional[str] = Field(None, description="JSON array of areas")
    products_used: Optional[str] = Field(None, description="JSON array of cleaning products")
    
    quality_check_done: bool = Field(default=False)
    quality_check_by: Optional[str] = Field(None, max_length=200)
    
    next_cleaning_due: Optional[str] = Field(None, max_length=20)
    notes: Optional[str] = None
    
    @validator('cleaning_type')
    def validate_cleaning_type(cls, v):
        valid = ['routine', 'deep', 'terminal', 'discharge', 'spot', 'disinfection']
        if v.lower() not in valid:
            raise ValueError(f"Cleaning type must be one of: {', '.join(valid)}")
        return v.lower()


# Room Maintenance Schema
class RoomMaintenanceSchema(BaseModel):
    maintenance_type: str = Field(..., max_length=50)
    reported_by: str = Field(..., max_length=200)
    reported_date: str = Field(..., max_length=20)
    
    issue_description: str = Field(..., description="Description of the issue")
    priority: str = Field(default='normal', max_length=20)
    
    scheduled_date: Optional[str] = Field(None, max_length=20)
    completed_date: Optional[str] = Field(None, max_length=20)
    
    assigned_to: Optional[str] = Field(None, max_length=200)
    work_done: Optional[str] = None
    parts_replaced: Optional[str] = None
    
    cost: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    
    status: str = Field(default='reported', max_length=20)
    notes: Optional[str] = None
    
    @validator('maintenance_type')
    def validate_maintenance_type(cls, v):
        valid = ['electrical', 'plumbing', 'ac', 'medical_equipment', 
                'furniture', 'painting', 'general', 'emergency']
        if v.lower() not in valid:
            raise ValueError(f"Maintenance type must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validator('priority')
    def validate_priority(cls, v):
        valid = ['low', 'normal', 'high', 'urgent', 'emergency']
        if v.lower() not in valid:
            raise ValueError(f"Priority must be one of: {', '.join(valid)}")
        return v.lower()
    
    @validator('status')
    def validate_status(cls, v):
        valid = ['reported', 'scheduled', 'in_progress', 'completed', 'cancelled']
        if v.lower() not in valid:
            raise ValueError(f"Status must be one of: {', '.join(valid)}")
        return v.lower()


# Room Status Update Schema
class RoomStatusUpdateSchema(BaseModel):
    status: str = Field(..., max_length=20)
    is_available: bool = Field(...)
    
    updated_by: str = Field(..., max_length=200)
    reason: Optional[str] = None
    expected_available_date: Optional[str] = Field(None, max_length=20)
    notes: Optional[str] = None
    
    @validator('status')
    def validate_status(cls, v):
        valid = [
            'available', 'occupied', 'maintenance', 'reserved',
            'cleaning', 'under_renovation', 'quarantine'
        ]
        if v.lower() not in valid:
            raise ValueError(f"Status must be one of: {', '.join(valid)}")
        return v.lower()


# Room Occupancy Update Schema
class RoomOccupancyUpdateSchema(BaseModel):
    occupancy_change: int = Field(..., description="Positive to increase, negative to decrease")
    reason: str = Field(..., max_length=200)
    updated_by: str = Field(..., max_length=200)
    notes: Optional[str] = None


# Room Pricing Update Schema
class RoomPricingUpdateSchema(BaseModel):
    price_per_day: condecimal(max_digits=10, decimal_places=2, ge=0) = Field(...)
    deposit_amount: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    
    effective_date: str = Field(..., max_length=20)
    updated_by: str = Field(..., max_length=200)
    reason: Optional[str] = None
    notes: Optional[str] = None


# Room Facilities Update Schema
class RoomFacilitiesUpdateSchema(BaseModel):
    # Room Specifications
    has_attached_bathroom: Optional[bool] = None
    has_ac: Optional[bool] = None
    has_window: Optional[bool] = None
    has_balcony: Optional[bool] = None
    has_tv: Optional[bool] = None
    has_telephone: Optional[bool] = None
    has_refrigerator: Optional[bool] = None
    
    # Medical Equipment
    has_oxygen_supply: Optional[bool] = None
    has_suction: Optional[bool] = None
    has_monitor: Optional[bool] = None
    has_ventilator: Optional[bool] = None
    
    updated_by: str = Field(..., max_length=200)
    update_date: str = Field(..., max_length=20)
    notes: Optional[str] = None


# Room with Beds Response
class RoomWithBedsResponse(RoomResponse):
    beds: list[dict]  # List of bed details
    available_bed_count: int
    occupied_bed_count: int


# Room Occupancy History Schema
class RoomOccupancyHistorySchema(BaseModel):
    room_id: int
    room_number: str
    date: str
    occupancy: int
    capacity: int
    occupancy_rate: float
    status: str


# Room Revenue Schema
class RoomRevenueSchema(BaseModel):
    room_id: int
    room_number: str
    room_type: str
    
    total_days_occupied: int
    price_per_day: Decimal
    total_revenue: Decimal
    
    period_start: str
    period_end: str
    
    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }


# Bulk Room Create Schema
class BulkRoomCreateSchema(BaseModel):
    room_prefix: str = Field(..., max_length=10, description="Prefix for room numbers")
    start_number: int = Field(..., ge=1)
    count: int = Field(..., ge=1, le=100)
    
    room_type: str = Field(..., max_length=50)
    floor_id: Optional[int] = None
    floor_number: Optional[int] = None
    ward_id: Optional[int] = None
    department_id: Optional[int] = None
    
    bed_capacity: int = Field(default=1, ge=1)
    
    # Default Specifications
    has_attached_bathroom: bool = Field(default=False)
    has_ac: bool = Field(default=False)
    has_oxygen_supply: bool = Field(default=False)
    
    price_per_day: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    
    created_by: str = Field(..., max_length=200)


# Floor-wise Room Distribution
class FloorRoomDistributionSchema(BaseModel):
    floor_number: int
    floor_display: str
    total_rooms: int
    available_rooms: int
    occupied_rooms: int
    maintenance_rooms: int
    
    rooms_by_type: dict  # {type: count}
    total_capacity: int
    current_occupancy: int
    occupancy_rate: float


# Room Allocation Suggestion Schema
class RoomAllocationSuggestionSchema(BaseModel):
    patient_type: str = Field(..., max_length=50)
    treatment_type: str = Field(..., max_length=50)
    
    isolation_required: bool = Field(default=False)
    oxygen_required: bool = Field(default=False)
    ventilator_required: bool = Field(default=False)
    monitoring_required: bool = Field(default=False)
    
    preferred_floor: Optional[int] = None
    preferred_ward: Optional[int] = None
    
    budget_per_day: Optional[Decimal] = None


# Room Allocation Suggestion Response
class RoomAllocationSuggestionResponse(BaseModel):
    suggested_rooms: list[RoomAvailabilityResponse]
    match_score: float
    reasoning: str