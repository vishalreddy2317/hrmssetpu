"""
Ambulance Schemas
Pydantic schemas for ambulance fleet management validation and serialization
"""

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, Any
from datetime import datetime, date
from decimal import Decimal
from enum import Enum
import re


# Enums
class VehicleType(str, Enum):
    """Valid vehicle types"""
    BASIC = "basic"
    ADVANCED = "advanced"
    AIR = "air"
    MOBILE_ICU = "mobile_icu"
    PATIENT_TRANSPORT = "patient_transport"
    NEONATAL = "neonatal"


class AmbulanceStatus(str, Enum):
    """Valid ambulance statuses"""
    AVAILABLE = "available"
    ON_DUTY = "on_duty"
    MAINTENANCE = "maintenance"
    OUT_OF_SERVICE = "out_of_service"
    RETIRED = "retired"


class FuelType(str, Enum):
    """Valid fuel types"""
    PETROL = "petrol"
    DIESEL = "diesel"
    CNG = "cng"
    ELECTRIC = "electric"
    HYBRID = "hybrid"


# Nested Schemas
class HospitalBasic(BaseModel):
    """Basic hospital info for nested responses"""
    id: int
    name: str
    city: Optional[str] = None
    phone: Optional[str] = None
    
    class Config:
        from_attributes = True


class LocationCoordinates(BaseModel):
    """GPS coordinates schema"""
    latitude: Decimal = Field(..., ge=-90, le=90, description="Latitude coordinate")
    longitude: Decimal = Field(..., ge=-180, le=180, description="Longitude coordinate")
    location_name: Optional[str] = Field(None, description="Human-readable location")
    
    class Config:
        json_schema_extra = {
            "example": {
                "latitude": 40.7128,
                "longitude": -74.0060,
                "location_name": "Downtown Hospital, New York"
            }
        }


# Equipment Schema
class AmbulanceEquipment(BaseModel):
    """Schema for ambulance equipment"""
    has_oxygen: bool = Field(default=True, description="Oxygen supply available")
    has_ventilator: bool = Field(default=False, description="Ventilator available")
    has_defibrillator: bool = Field(default=False, description="Defibrillator available")
    has_ecg: bool = Field(default=False, description="ECG machine available")
    has_stretcher: bool = Field(default=True, description="Stretcher available")
    has_wheelchair: bool = Field(default=True, description="Wheelchair available")
    
    class Config:
        json_schema_extra = {
            "example": {
                "has_oxygen": True,
                "has_ventilator": True,
                "has_defibrillator": True,
                "has_ecg": True,
                "has_stretcher": True,
                "has_wheelchair": True
            }
        }


# Driver Schema
class DriverInfo(BaseModel):
    """Driver information schema"""
    driver_name: Optional[str] = Field(None, max_length=200, description="Driver name")
    driver_phone: Optional[str] = Field(None, max_length=20, description="Driver phone number")
    driver_license: Optional[str] = Field(None, max_length=50, description="Driver license number")
    
    @field_validator('driver_phone')
    @classmethod
    def validate_phone(cls, v):
        """Basic phone validation"""
        if v is None:
            return None
        # Remove spaces and dashes
        cleaned = re.sub(r'[\s\-\(\)]', '', v)
        if not re.match(r'^\+?[0-9]{10,15}$', cleaned):
            raise ValueError("Invalid phone number format")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "driver_name": "John Driver",
                "driver_phone": "+1-555-123-4567",
                "driver_license": "DL12345678"
            }
        }


# Maintenance Schema
class MaintenanceInfo(BaseModel):
    """Maintenance information schema"""
    last_maintenance_date: Optional[str] = Field(None, description="Last maintenance date (YYYY-MM-DD)")
    next_maintenance_date: Optional[str] = Field(None, description="Next scheduled maintenance (YYYY-MM-DD)")
    mileage: Optional[int] = Field(None, ge=0, description="Current mileage in kilometers")
    
    @field_validator('last_maintenance_date', 'next_maintenance_date')
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
    
    class Config:
        json_schema_extra = {
            "example": {
                "last_maintenance_date": "2024-01-01",
                "next_maintenance_date": "2024-04-01",
                "mileage": 45000
            }
        }


# Base Schema
class AmbulanceBase(BaseModel):
    """Base schema with common fields"""
    # Vehicle Details
    ambulance_number: str = Field(..., max_length=20, description="Unique ambulance identifier")
    vehicle_number: str = Field(..., max_length=20, description="Vehicle registration/plate number")
    vehicle_type: VehicleType = Field(..., description="Type of ambulance vehicle")
    
    # Vehicle Information
    manufacturer: Optional[str] = Field(None, max_length=100, description="Vehicle manufacturer")
    model: Optional[str] = Field(None, max_length=100, description="Vehicle model")
    year: Optional[int] = Field(None, ge=1900, le=2100, description="Manufacturing year")
    color: Optional[str] = Field(None, max_length=50, description="Vehicle color")
    
    # Hospital
    hospital_id: Optional[int] = Field(None, description="Associated hospital ID")
    
    # Driver Details
    driver_name: Optional[str] = Field(None, max_length=200, description="Current driver name")
    driver_phone: Optional[str] = Field(None, max_length=20, description="Driver phone")
    driver_license: Optional[str] = Field(None, max_length=50, description="Driver license number")
    
    # Equipment
    has_oxygen: bool = Field(default=True, description="Has oxygen supply")
    has_ventilator: bool = Field(default=False, description="Has ventilator")
    has_defibrillator: bool = Field(default=False, description="Has defibrillator")
    has_ecg: bool = Field(default=False, description="Has ECG machine")
    has_stretcher: bool = Field(default=True, description="Has stretcher")
    has_wheelchair: bool = Field(default=True, description="Has wheelchair")
    
    # Capacity
    patient_capacity: int = Field(default=1, gt=0, description="Patient capacity")
    staff_capacity: int = Field(default=2, ge=0, description="Staff capacity")
    
    # Status
    status: AmbulanceStatus = Field(default=AmbulanceStatus.AVAILABLE, description="Current status")
    is_available: bool = Field(default=True, description="Availability flag")
    
    # Current Location
    current_latitude: Optional[Decimal] = Field(None, ge=-90, le=90, description="Current latitude")
    current_longitude: Optional[Decimal] = Field(None, ge=-180, le=180, description="Current longitude")
    current_location: Optional[str] = Field(None, max_length=500, description="Current location description")
    
    # Maintenance
    last_maintenance_date: Optional[str] = Field(None, description="Last maintenance date")
    next_maintenance_date: Optional[str] = Field(None, description="Next maintenance date")
    mileage: Optional[int] = Field(None, ge=0, description="Current mileage (km)")
    
    # Insurance
    insurance_number: Optional[str] = Field(None, max_length=100, description="Insurance policy number")
    insurance_expiry: Optional[str] = Field(None, description="Insurance expiry date")
    
    # Registration
    registration_number: Optional[str] = Field(None, max_length=50, description="Vehicle registration number")
    registration_expiry: Optional[str] = Field(None, description="Registration expiry date")
    
    # Cost
    fuel_type: Optional[FuelType] = Field(None, description="Fuel type")
    base_charge: Optional[Decimal] = Field(None, ge=0, decimal_places=2, description="Base service charge")
    per_km_charge: Optional[Decimal] = Field(None, ge=0, decimal_places=2, description="Per kilometer charge")
    
    # Notes
    notes: Optional[str] = Field(None, description="Additional notes")

    @field_validator('vehicle_number', 'ambulance_number')
    @classmethod
    def validate_uppercase(cls, v):
        """Convert to uppercase for consistency"""
        return v.upper() if v else v
    
    @field_validator('last_maintenance_date', 'next_maintenance_date', 
                     'insurance_expiry', 'registration_expiry')
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
    
    @field_validator('driver_phone')
    @classmethod
    def validate_phone(cls, v):
        """Basic phone validation"""
        if v is None:
            return None
        cleaned = re.sub(r'[\s\-\(\)]', '', v)
        if not re.match(r'^\+?[0-9]{10,15}$', cleaned):
            raise ValueError("Invalid phone number format")
        return v
    
    @model_validator(mode='after')
    def validate_location_coordinates(self):
        """Ensure both lat/long are provided together"""
        if (self.current_latitude is not None) != (self.current_longitude is not None):
            raise ValueError("Both latitude and longitude must be provided together")
        return self
    
    @model_validator(mode='after')
    def validate_availability(self):
        """Ensure status and availability are consistent"""
        if self.status in [AmbulanceStatus.MAINTENANCE, AmbulanceStatus.OUT_OF_SERVICE, AmbulanceStatus.RETIRED]:
            self.is_available = False
        elif self.status == AmbulanceStatus.AVAILABLE:
            self.is_available = True
        return self


# Create Schema
class AmbulanceCreate(AmbulanceBase):
    """Schema for creating new ambulance"""
    
    class Config:
        json_schema_extra = {
            "example": {
                "ambulance_number": "AMB-001",
                "vehicle_number": "NY-1234-AB",
                "vehicle_type": "advanced",
                "manufacturer": "Mercedes-Benz",
                "model": "Sprinter",
                "year": 2023,
                "color": "White",
                "hospital_id": 1,
                "driver_name": "John Driver",
                "driver_phone": "+1-555-123-4567",
                "driver_license": "DL12345678",
                "has_oxygen": True,
                "has_ventilator": True,
                "has_defibrillator": True,
                "has_ecg": True,
                "has_stretcher": True,
                "has_wheelchair": True,
                "patient_capacity": 2,
                "staff_capacity": 3,
                "fuel_type": "diesel",
                "base_charge": 500.00,
                "per_km_charge": 10.00,
                "insurance_number": "INS-2024-12345",
                "insurance_expiry": "2025-12-31",
                "registration_number": "REG-2024-001",
                "registration_expiry": "2025-12-31"
            }
        }


# Update Schema
class AmbulanceUpdate(BaseModel):
    """Schema for updating ambulance (partial updates allowed)"""
    vehicle_type: Optional[VehicleType] = None
    manufacturer: Optional[str] = Field(None, max_length=100)
    model: Optional[str] = Field(None, max_length=100)
    year: Optional[int] = Field(None, ge=1900, le=2100)
    color: Optional[str] = Field(None, max_length=50)
    hospital_id: Optional[int] = None
    
    # Driver
    driver_name: Optional[str] = Field(None, max_length=200)
    driver_phone: Optional[str] = Field(None, max_length=20)
    driver_license: Optional[str] = Field(None, max_length=50)
    
    # Equipment
    has_oxygen: Optional[bool] = None
    has_ventilator: Optional[bool] = None
    has_defibrillator: Optional[bool] = None
    has_ecg: Optional[bool] = None
    has_stretcher: Optional[bool] = None
    has_wheelchair: Optional[bool] = None
    
    # Capacity
    patient_capacity: Optional[int] = Field(None, gt=0)
    staff_capacity: Optional[int] = Field(None, ge=0)
    
    # Status
    status: Optional[AmbulanceStatus] = None
    is_available: Optional[bool] = None
    
    # Location
    current_latitude: Optional[Decimal] = Field(None, ge=-90, le=90)
    current_longitude: Optional[Decimal] = Field(None, ge=-180, le=180)
    current_location: Optional[str] = Field(None, max_length=500)
    
    # Maintenance
    last_maintenance_date: Optional[str] = None
    next_maintenance_date: Optional[str] = None
    mileage: Optional[int] = Field(None, ge=0)
    
    # Insurance
    insurance_number: Optional[str] = Field(None, max_length=100)
    insurance_expiry: Optional[str] = None
    
    # Registration
    registration_number: Optional[str] = Field(None, max_length=50)
    registration_expiry: Optional[str] = None
    
    # Cost
    fuel_type: Optional[FuelType] = None
    base_charge: Optional[Decimal] = Field(None, ge=0)
    per_km_charge: Optional[Decimal] = Field(None, ge=0)
    
    # Notes
    notes: Optional[str] = None

    @field_validator('driver_phone')
    @classmethod
    def validate_phone(cls, v):
        if v is None:
            return None
        cleaned = re.sub(r'[\s\-\(\)]', '', v)
        if not re.match(r'^\+?[0-9]{10,15}$', cleaned):
            raise ValueError("Invalid phone number format")
        return v


# Response Schema
class AmbulanceResponse(AmbulanceBase):
    """Schema for ambulance response"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "ambulance_number": "AMB-001",
                "vehicle_number": "NY-1234-AB",
                "vehicle_type": "advanced",
                "manufacturer": "Mercedes-Benz",
                "model": "Sprinter",
                "year": 2023,
                "color": "White",
                "status": "available",
                "is_available": True,
                "patient_capacity": 2,
                "staff_capacity": 3,
                "has_oxygen": True,
                "has_ventilator": True,
                "base_charge": 500.00,
                "per_km_charge": 10.00,
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00"
            }
        }


# Detailed Response with Relationships
class AmbulanceDetailResponse(AmbulanceResponse):
    """Detailed ambulance response with nested relationships"""
    hospital: Optional[HospitalBasic] = None
    
    class Config:
        from_attributes = True


# List Response Schema
class AmbulanceListResponse(BaseModel):
    """Schema for paginated list of ambulances"""
    total: int = Field(..., description="Total number of records")
    page: int = Field(..., ge=1, description="Current page number")
    page_size: int = Field(..., ge=1, le=100, description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")
    items: list[AmbulanceResponse] = Field(..., description="Ambulance items")


# Filter/Query Schema
class AmbulanceFilter(BaseModel):
    """Schema for filtering ambulances"""
    # ID filters
    hospital_id: Optional[int] = Field(None, description="Filter by hospital ID")
    
    # String filters
    ambulance_number: Optional[str] = Field(None, description="Filter by ambulance number")
    vehicle_number: Optional[str] = Field(None, description="Filter by vehicle number")
    driver_name: Optional[str] = Field(None, description="Filter by driver name")
    
    # Enum filters
    vehicle_type: Optional[VehicleType] = Field(None, description="Filter by vehicle type")
    status: Optional[AmbulanceStatus] = Field(None, description="Filter by status")
    fuel_type: Optional[FuelType] = Field(None, description="Filter by fuel type")
    
    # Boolean filters
    is_available: Optional[bool] = Field(None, description="Filter by availability")
    has_oxygen: Optional[bool] = Field(None, description="Filter by oxygen availability")
    has_ventilator: Optional[bool] = Field(None, description="Filter by ventilator")
    has_defibrillator: Optional[bool] = Field(None, description="Filter by defibrillator")
    has_ecg: Optional[bool] = Field(None, description="Filter by ECG")
    
    # Range filters
    year_from: Optional[int] = Field(None, description="Vehicle year from")
    year_to: Optional[int] = Field(None, description="Vehicle year to")
    mileage_max: Optional[int] = Field(None, description="Maximum mileage")
    
    # Maintenance filters
    maintenance_due: Optional[bool] = Field(None, description="Maintenance due soon")
    insurance_expiring: Optional[bool] = Field(None, description="Insurance expiring soon")
    
    # Location filter (for nearby search)
    near_latitude: Optional[Decimal] = Field(None, description="Search near latitude")
    near_longitude: Optional[Decimal] = Field(None, description="Search near longitude")
    radius_km: Optional[float] = Field(None, gt=0, description="Search radius in km")
    
    # Search
    search: Optional[str] = Field(None, description="Search in ambulance/vehicle number, driver name")
    
    # Pagination
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")
    
    # Sorting
    sort_by: Optional[str] = Field("ambulance_number", description="Field to sort by")
    sort_order: Optional[str] = Field("asc", pattern="^(asc|desc)$", description="Sort order")
    
    # Include relationships
    include_hospital: bool = Field(False, description="Include hospital details")


# Location Update Schema
class UpdateLocation(BaseModel):
    """Schema for updating ambulance location"""
    latitude: Decimal = Field(..., ge=-90, le=90, description="Current latitude")
    longitude: Decimal = Field(..., ge=-180, le=180, description="Current longitude")
    location_name: Optional[str] = Field(None, max_length=500, description="Location description")
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Location timestamp")


# Status Update Schema
class UpdateStatus(BaseModel):
    """Schema for updating ambulance status"""
    status: AmbulanceStatus = Field(..., description="New status")
    reason: Optional[str] = Field(None, description="Reason for status change")
    notes: Optional[str] = Field(None, description="Additional notes")


# Dispatch Schema
class DispatchAmbulance(BaseModel):
    """Schema for dispatching an ambulance"""
    emergency_id: Optional[int] = Field(None, description="Emergency request ID")
    pickup_location: str = Field(..., description="Pickup location")
    pickup_latitude: Optional[Decimal] = Field(None, ge=-90, le=90)
    pickup_longitude: Optional[Decimal] = Field(None, ge=-180, le=180)
    destination: str = Field(..., description="Destination")
    destination_latitude: Optional[Decimal] = Field(None, ge=-90, le=90)
    destination_longitude: Optional[Decimal] = Field(None, ge=-180, le=180)
    patient_name: Optional[str] = Field(None, description="Patient name")
    patient_condition: Optional[str] = Field(None, description="Patient condition")
    priority: str = Field(default="normal", pattern="^(low|normal|high|critical)$", description="Priority level")
    estimated_arrival_time: Optional[str] = Field(None, description="ETA to pickup")
    notes: Optional[str] = Field(None, description="Dispatch notes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "emergency_id": 123,
                "pickup_location": "123 Main St, New York",
                "pickup_latitude": 40.7128,
                "pickup_longitude": -74.0060,
                "destination": "Central Hospital, New York",
                "destination_latitude": 40.7589,
                "destination_longitude": -73.9851,
                "patient_name": "John Doe",
                "patient_condition": "Chest pain, difficulty breathing",
                "priority": "critical",
                "estimated_arrival_time": "10 minutes",
                "notes": "Patient is conscious but in pain"
            }
        }


# Maintenance Record Schema
class MaintenanceRecord(BaseModel):
    """Schema for recording maintenance"""
    maintenance_date: str = Field(..., description="Maintenance date")
    maintenance_type: str = Field(..., description="Type of maintenance")
    description: str = Field(..., description="Maintenance description")
    cost: Optional[Decimal] = Field(None, ge=0, description="Maintenance cost")
    performed_by: Optional[str] = Field(None, description="Performed by (mechanic/service center)")
    mileage_at_maintenance: Optional[int] = Field(None, ge=0, description="Mileage at maintenance")
    next_maintenance_due: Optional[str] = Field(None, description="Next maintenance due date")
    parts_replaced: Optional[str] = Field(None, description="Parts replaced")
    notes: Optional[str] = Field(None, description="Additional notes")
    
    @field_validator('maintenance_date', 'next_maintenance_due')
    @classmethod
    def validate_date(cls, v):
        if v is None:
            return None
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")


# Statistics Schema
class AmbulanceStats(BaseModel):
    """Schema for ambulance statistics"""
    total_ambulances: int
    available_ambulances: int
    on_duty_ambulances: int
    in_maintenance: int
    out_of_service: int
    ambulances_by_type: dict[str, int]
    ambulances_by_hospital: dict[str, int]
    average_mileage: Optional[float] = None
    maintenance_due_soon: int
    insurance_expiring_soon: int
    registration_expiring_soon: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_ambulances": 50,
                "available_ambulances": 30,
                "on_duty_ambulances": 15,
                "in_maintenance": 3,
                "out_of_service": 2,
                "ambulances_by_type": {
                    "basic": 20,
                    "advanced": 15,
                    "mobile_icu": 10,
                    "air": 5
                },
                "ambulances_by_hospital": {
                    "Central Hospital": 25,
                    "City Hospital": 15,
                    "General Hospital": 10
                },
                "average_mileage": 45000.5,
                "maintenance_due_soon": 5,
                "insurance_expiring_soon": 3,
                "registration_expiring_soon": 2
            }
        }


# Dashboard Schema
class AmbulanceDashboard(BaseModel):
    """Dashboard summary for ambulance fleet"""
    total_fleet: int
    currently_available: int
    currently_dispatched: int
    response_time_avg: Optional[float] = Field(None, description="Average response time in minutes")
    trips_today: int
    trips_this_month: int
    fuel_consumption_month: Optional[Decimal] = None
    maintenance_alerts: int
    critical_alerts: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_fleet": 50,
                "currently_available": 30,
                "currently_dispatched": 15,
                "response_time_avg": 8.5,
                "trips_today": 45,
                "trips_this_month": 1250,
                "fuel_consumption_month": 5000.00,
                "maintenance_alerts": 5,
                "critical_alerts": 2
            }
        }


# Available Ambulances Response (for dispatch)
class AvailableAmbulance(BaseModel):
    """Schema for available ambulances with distance"""
    id: int
    ambulance_number: str
    vehicle_number: str
    vehicle_type: VehicleType
    driver_name: Optional[str] = None
    driver_phone: Optional[str] = None
    current_location: Optional[str] = None
    distance_km: Optional[float] = Field(None, description="Distance from pickup point")
    estimated_arrival_minutes: Optional[int] = Field(None, description="Estimated arrival time")
    equipment_score: Optional[int] = Field(None, description="Equipment capability score")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "ambulance_number": "AMB-001",
                "vehicle_number": "NY-1234-AB",
                "vehicle_type": "advanced",
                "driver_name": "John Driver",
                "driver_phone": "+1-555-123-4567",
                "current_location": "Downtown, New York",
                "distance_km": 2.5,
                "estimated_arrival_minutes": 7,
                "equipment_score": 95
            }
        }


# Fuel Tracking Schema
class FuelRecord(BaseModel):
    """Schema for fuel consumption tracking"""
    refuel_date: str = Field(..., description="Refueling date")
    fuel_quantity: Decimal = Field(..., gt=0, description="Fuel quantity in liters")
    fuel_cost: Decimal = Field(..., gt=0, description="Fuel cost")
    mileage_at_refuel: int = Field(..., ge=0, description="Mileage at refueling")
    fuel_station: Optional[str] = Field(None, description="Fuel station name")
    notes: Optional[str] = Field(None, description="Additional notes")
    
    @field_validator('refuel_date')
    @classmethod
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")


# Trip Record Schema
class TripRecord(BaseModel):
    """Schema for ambulance trip/journey record"""
    trip_date: str = Field(..., description="Trip date")
    start_time: str = Field(..., description="Start time")
    end_time: Optional[str] = Field(None, description="End time")
    pickup_location: str = Field(..., description="Pickup location")
    drop_location: str = Field(..., description="Drop location")
    distance_km: Optional[Decimal] = Field(None, ge=0, description="Distance covered")
    patient_name: Optional[str] = Field(None, description="Patient name")
    emergency_type: Optional[str] = Field(None, description="Type of emergency")
    driver_name: Optional[str] = Field(None, description="Driver name")
    cost: Optional[Decimal] = Field(None, ge=0, description="Trip cost")
    payment_status: Optional[str] = Field(None, description="Payment status")
    notes: Optional[str] = Field(None, description="Trip notes")