"""
SQLAlchemy Models for Hospital Management System
All models use SQLAlchemy 2.0 syntax with PostgreSQL
"""

from app.core.database import Base

# Import all models for Alembic migration detection
from .base import BaseModel, TimestampMixin, SoftDeleteMixin
from .floor import Floor
from .hospital import Hospital
from .branch import Branch
from .department import Department
from .ward import Ward
from .room import Room
from .bed import Bed
from .patient import Patient
from .doctor import Doctor
from .nurse import Nurse
from .staff import Staff
from .appointment import Appointment
from .admission import Admission
from .discharge import Discharge
from .lab_test import LabTest
from .lab_report import LabReport
from .medicine import Medicine
from .prescription import Prescription
from .pharmacy import Pharmacy
from .billing import Billing
from .payment import Payment
from .insurance import Insurance
from .ambulance import Ambulance
from .emergency import Emergency
from .operation import Operation
from .imaging import Imaging
from .equipment import Equipment
from .inventory import Inventory
from .supplier import Supplier
from .vendor import Vendor
from .purchase_order import PurchaseOrder
from .expense import Expense
from .revenue import Revenue
from .attendance import Attendance
from .leave import Leave
from .shift import Shift
from .schedule import Schedule
from .payroll import Payroll
from .event import Event
from .notification import Notification
from .message import Message
from .chat import Chat
from .complaint import Complaint
from .feedback import Feedback
from .faq import FAQ
from .setting import Setting
from .role import Role
from .role_permission import RolePermission
from .api_key import APIKey
from .audit_log import AuditLog
from .activity_log import ActivityLog

__all__ = [
    # Base
    "Base",
    "BaseModel",
    "TimestampMixin",
    "SoftDeleteMixin",
    
    # Core Infrastructure
    "Floor",
    "Hospital",
    "Branch",
    "Department",
    "Ward",
    "Room",
    "Bed",
    
    # People
    "Patient",
    "Doctor",
    "Nurse",
    "Staff",
    
    # Medical Services
    "Appointment",
    "Admission",
    "Discharge",
    "LabTest",
    "LabReport",
    "Medicine",
    "Prescription",
    "Pharmacy",
    "Emergency",
    "Operation",
    "Imaging",
    
    # Financial
    "Billing",
    "Payment",
    "Insurance",
    "Expense",
    "Revenue",
    "Payroll",
    
    # Resources
    "Ambulance",
    "Equipment",
    "Inventory",
    "Supplier",
    "Vendor",
    "PurchaseOrder",
    
    # HR Management
    "Attendance",
    "Leave",
    "Shift",
    "Schedule",
    
    # Communication
    "Event",
    "Notification",
    "Message",
    "Chat",
    "Complaint",
    "Feedback",
    "FAQ",
    
    # System
    "Setting",
    "Role",
    "RolePermission",
    "APIKey",
    "AuditLog",
    "ActivityLog",
]
