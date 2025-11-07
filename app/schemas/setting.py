"""
Setting Schemas
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Any
from datetime import datetime


# Base Schema
class SettingBase(BaseModel):
    setting_key: str = Field(..., max_length=100, description="Unique setting key")
    category: str = Field(..., max_length=50)
    
    @validator('category')
    def validate_category(cls, v):
        valid = [
            'general', 'email', 'sms', 'payment', 'notification',
            'security', 'appearance', 'appointment', 'billing', 'system'
        ]
        if v.lower() not in valid:
            raise ValueError(f"Category must be one of: {', '.join(valid)}")
        return v.lower()


# Create Schema
class SettingCreate(SettingBase):
    setting_value: str = Field(..., description="Setting value")
    
    data_type: str = Field(default='string', max_length=20)
    description: Optional[str] = None
    
    is_sensitive: bool = Field(default=False)
    is_editable: bool = Field(default=True)
    
    default_value: Optional[str] = None
    validation_rules: Optional[str] = Field(None, description="JSON format")
    
    modified_by: Optional[str] = Field(None, max_length=200)
    
    @validator('data_type')
    def validate_data_type(cls, v):
        valid = ['string', 'integer', 'boolean', 'json', 'float', 'array']
        if v.lower() not in valid:
            raise ValueError(f"Data type must be one of: {', '.join(valid)}")
        return v.lower()


# Update Schema
class SettingUpdate(BaseModel):
    setting_value: Optional[str] = None
    description: Optional[str] = None
    
    is_editable: Optional[bool] = None
    validation_rules: Optional[str] = None
    
    modified_by: Optional[str] = Field(None, max_length=200)


# Response Schema
class SettingResponse(SettingBase):
    id: int
    setting_value: str
    
    data_type: str
    description: Optional[str]
    
    is_sensitive: bool
    is_editable: bool
    
    default_value: Optional[str]
    validation_rules: Optional[str]
    
    modified_by: Optional[str]
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# Sensitive Setting Response (value masked)
class SettingSensitiveResponse(BaseModel):
    id: int
    setting_key: str
    setting_value: str = "***HIDDEN***"
    
    data_type: str
    category: str
    description: Optional[str]
    
    is_sensitive: bool = True
    is_editable: bool
    
    class Config:
        from_attributes = True


# List Response
class SettingListResponse(BaseModel):
    total: int
    items: list[SettingResponse]
    page: int
    page_size: int
    total_pages: int


# Settings by Category Response
class SettingsByCategoryResponse(BaseModel):
    category: str
    settings: list[SettingResponse]
    total: int


# All Settings Grouped
class AllSettingsGroupedResponse(BaseModel):
    general: list[SettingResponse]
    email: list[SettingResponse]
    sms: list[SettingResponse]
    payment: list[SettingResponse]
    notification: list[SettingResponse]
    security: list[SettingResponse]
    appearance: list[SettingResponse]
    appointment: list[SettingResponse]
    billing: list[SettingResponse]
    system: list[SettingResponse]


# Bulk Update Schema
class BulkSettingUpdateSchema(BaseModel):
    settings: list[dict] = Field(..., min_items=1, description="List of {key, value}")
    modified_by: str = Field(..., max_length=200)
    
    @validator('settings')
    def validate_settings(cls, v):
        for setting in v:
            if 'setting_key' not in setting or 'setting_value' not in setting:
                raise ValueError("Each setting must have 'setting_key' and 'setting_value'")
        return v


# Reset Setting Schema
class ResetSettingSchema(BaseModel):
    setting_key: str = Field(..., max_length=100)
    reset_by: str = Field(..., max_length=200)


# Import Settings Schema
class ImportSettingsSchema(BaseModel):
    settings_json: str = Field(..., description="JSON string of settings")
    overwrite_existing: bool = Field(default=False)
    imported_by: str = Field(..., max_length=200)


# Export Settings Schema
class ExportSettingsSchema(BaseModel):
    categories: Optional[list[str]] = Field(None, description="Categories to export, None for all")
    include_sensitive: bool = Field(default=False)
    exported_by: str = Field(..., max_length=200)


# Setting Value Schema (for getting parsed value)
class SettingValueSchema(BaseModel):
    setting_key: str
    value: Any  # Parsed based on data_type
    data_type: str


# Validate Setting Schema
class ValidateSettingSchema(BaseModel):
    setting_key: str = Field(..., max_length=100)
    setting_value: str = Field(...)
    
    
# Validate Setting Response
class ValidateSettingResponse(BaseModel):
    is_valid: bool
    errors: Optional[list[str]]
    parsed_value: Optional[Any]


# Setting Template Schema
class SettingTemplateSchema(BaseModel):
    template_name: str = Field(..., description="hospital_basic, clinic, diagnostic_center")
    settings: list[dict]


# Common Settings Schemas

# Email Settings
class EmailSettingsSchema(BaseModel):
    smtp_host: str = Field(..., max_length=200)
    smtp_port: int = Field(..., ge=1, le=65535)
    smtp_username: str = Field(..., max_length=200)
    smtp_password: str = Field(..., max_length=200)
    
    from_email: str = Field(..., max_length=200)
    from_name: str = Field(..., max_length=200)
    
    use_tls: bool = Field(default=True)
    use_ssl: bool = Field(default=False)


# SMS Settings
class SMSSettingsSchema(BaseModel):
    provider: str = Field(..., max_length=50, description="twilio, msg91, etc.")
    api_key: str = Field(..., max_length=200)
    api_secret: str = Field(..., max_length=200)
    
    sender_id: str = Field(..., max_length=20)
    
    enable_appointment_sms: bool = Field(default=True)
    enable_billing_sms: bool = Field(default=True)
    enable_report_sms: bool = Field(default=True)


# Payment Settings
class PaymentSettingsSchema(BaseModel):
    enable_online_payment: bool = Field(default=True)
    
    # Payment Gateway
    payment_gateway: str = Field(..., max_length=50, description="razorpay, stripe, paypal")
    gateway_api_key: str = Field(..., max_length=200)
    gateway_api_secret: str = Field(..., max_length=200)
    
    # Payment Methods
    accept_cash: bool = Field(default=True)
    accept_card: bool = Field(default=True)
    accept_upi: bool = Field(default=True)
    accept_insurance: bool = Field(default=True)
    
    # Tax
    tax_percentage: float = Field(default=0.0, ge=0, le=100)
    tax_number: Optional[str] = Field(None, max_length=50)


# Notification Settings
class NotificationSettingsSchema(BaseModel):
    enable_email_notifications: bool = Field(default=True)
    enable_sms_notifications: bool = Field(default=True)
    enable_push_notifications: bool = Field(default=True)
    enable_in_app_notifications: bool = Field(default=True)
    
    # Appointment Notifications
    appointment_reminder_hours: int = Field(default=24, ge=1)
    appointment_confirmation_required: bool = Field(default=True)
    
    # Billing Notifications
    send_billing_invoice: bool = Field(default=True)
    send_payment_receipt: bool = Field(default=True)
    
    # Report Notifications
    notify_lab_report_ready: bool = Field(default=True)
    notify_radiology_report_ready: bool = Field(default=True)


# Appointment Settings
class AppointmentSettingsSchema(BaseModel):
    default_appointment_duration: int = Field(default=30, ge=5, description="Minutes")
    allow_online_booking: bool = Field(default=True)
    
    booking_advance_days: int = Field(default=30, ge=1, description="How many days in advance")
    cancellation_hours: int = Field(default=24, ge=0, description="Minimum hours for cancellation")
    
    max_appointments_per_slot: int = Field(default=1, ge=1)
    enable_waiting_list: bool = Field(default=True)
    
    require_payment_for_booking: bool = Field(default=False)
    booking_deposit_amount: Optional[float] = Field(None, ge=0)


# General Settings
class GeneralSettingsSchema(BaseModel):
    hospital_name: str = Field(..., max_length=200)
    hospital_address: str = Field(...)
    hospital_city: str = Field(..., max_length=100)
    hospital_state: str = Field(..., max_length=100)
    hospital_country: str = Field(..., max_length=100)
    hospital_pincode: str = Field(..., max_length=20)
    
    hospital_phone: str = Field(..., max_length=20)
    hospital_email: str = Field(..., max_length=200)
    hospital_website: Optional[str] = Field(None, max_length=200)
    
    hospital_logo_url: Optional[str] = Field(None, max_length=500)
    
    timezone: str = Field(default="Asia/Kolkata", max_length=50)
    date_format: str = Field(default="YYYY-MM-DD", max_length=20)
    time_format: str = Field(default="HH:mm", max_length=20)
    currency: str = Field(default="INR", max_length=10)