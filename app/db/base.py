"""
✅ Import all models here for SQLAlchemy to discover them
UPDATED: Added 15 new models
"""
from app.models.base import Base

# -------------------------------------------------------------------------
# 🔹 Import User from auth module (source of truth)
# -------------------------------------------------------------------------
from app.auth.models import User, OTPCode

# -------------------------------------------------------------------------
# 🔹 Import all existing models
# -------------------------------------------------------------------------
from app.models.activity_log import ActivityLog
from app.models.ambulance import Ambulance
from app.models.api_key import APIKey
from app.models.appointment import Appointment
from app.models.attendance import Attendance
from app.models.audit_log import AuditLog
from app.models.bed import Bed
from app.models.billing import Billing
from app.models.chat import Chat
from app.models.complaint import Complaint
from app.models.department import Department
from app.models.diagnosis import Diagnosis
from app.models.doctor import Doctor
from app.models.event import Event
from app.models.faq import FAQ
from app.models.feedback import Feedback
from app.models.imaging import Imaging
from app.models.insurance import Insurance
from app.models.inventory import Inventory
from app.models.lab_report import LabReport
from app.models.lab_test import LabTest
from app.models.leave import Leave
from app.models.medical_record import MedicalRecord
from app.models.medicine import Medicine
from app.models.message import Message
from app.models.notification import Notification
from app.models.nurse import Nurse
from app.models.patient import Patient
from app.models.payment import Payment
from app.models.payroll import Payroll
from app.models.pharmacy import Pharmacy
from app.models.prescription import Prescription
from app.models.procedure import Procedure
from app.models.purchase_order import PurchaseOrder
from app.models.radiology import Radiology
from app.models.role import Role
from app.models.role_permission import RolePermission
from app.models.schedule import Schedule
from app.models.setting import Setting
from app.models.shift import Shift
from app.models.stock import Stock
from app.models.supplier import Supplier
from app.models.transport import Transport
from app.models.vendor import Vendor
from app.models.ward import Ward

# -------------------------------------------------------------------------
# 🔹 ✨ NEW: Import 15 new models ✨
# -------------------------------------------------------------------------
from app.models.admission import Admission
from app.models.branch import Branch
from app.models.discharge import Discharge
from app.models.emergency import Emergency
from app.models.equipment import Equipment
from app.models.expense import Expense
from app.models.hospital import Hospital
from app.models.maintenance import Maintenance
from app.models.operation import Operation
from app.models.revenue import Revenue
from app.models.room import Room
from app.models.staff import Staff
from app.models.technician import Technician
from app.models.test_result import TestResult
from app.models.vaccine import Vaccine