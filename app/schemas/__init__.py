"""
Pydantic V2 Schemas for Hospital Management System
All schemas use Pydantic V2 syntax and features
"""

from .base import ResponseModel, PaginatedResponse, StatusResponse
from .user import UserCreate, UserUpdate, UserResponse, UserLogin, TokenResponse
from .floor import FloorCreate, FloorUpdate, FloorResponse, FloorListResponse, FloorDetailResponse
from .hospital import HospitalCreate, HospitalUpdate, HospitalResponse, HospitalDetailResponse
from .branch import BranchCreate, BranchUpdate, BranchResponse
from .department import DepartmentCreate, DepartmentUpdate, DepartmentResponse, DepartmentDetailResponse
from .ward import WardCreate, WardUpdate, WardResponse, WardDetailResponse
from .room import RoomCreate, RoomUpdate, RoomResponse, RoomDetailResponse
from .bed import BedCreate, BedUpdate, BedResponse, BedAssignment
from .patient import PatientCreate, PatientUpdate, PatientResponse, PatientDetailResponse
from .doctor import DoctorCreate, DoctorUpdate, DoctorResponse, DoctorDetailResponse
from .nurse import NurseCreate, NurseUpdate, NurseResponse
from .staff import StaffCreate, StaffUpdate, StaffResponse
from .appointment import AppointmentCreate, AppointmentUpdate, AppointmentResponse, AppointmentDetailResponse
from .admission import AdmissionCreate, AdmissionUpdate, AdmissionResponse, AdmissionDetailResponse
from .discharge import DischargeCreate, DischargeUpdate, DischargeResponse
from .lab_test import LabTestCreate, LabTestUpdate, LabTestResponse
from .lab_report import LabReportCreate, LabReportUpdate, LabReportResponse
from .medicine import MedicineCreate, MedicineUpdate, MedicineResponse
from .prescription import PrescriptionCreate, PrescriptionUpdate, PrescriptionResponse
from .pharmacy import PharmacyCreate, PharmacyUpdate, PharmacyResponse
from .billing import BillingCreate, BillingUpdate, BillingResponse, BillingDetailResponse
from .payment import PaymentCreate, PaymentUpdate, PaymentResponse
from .insurance import InsuranceCreate, InsuranceUpdate, InsuranceResponse
from .ambulance import AmbulanceCreate, AmbulanceUpdate, AmbulanceResponse
from .emergency import EmergencyCreate, EmergencyUpdate, EmergencyResponse
from .operation import OperationCreate, OperationUpdate, OperationResponse
from .imaging import ImagingCreate, ImagingUpdate, ImagingResponse
from .equipment import EquipmentCreate, EquipmentUpdate, EquipmentResponse
from .inventory import InventoryCreate, InventoryUpdate, InventoryResponse
from .supplier import SupplierCreate, SupplierUpdate, SupplierResponse
from .vendor import VendorCreate, VendorUpdate, VendorResponse
from .purchase_order import PurchaseOrderCreate, PurchaseOrderUpdate, PurchaseOrderResponse
from .expense import ExpenseCreate, ExpenseUpdate, ExpenseResponse
from .revenue import RevenueCreate, RevenueUpdate, RevenueResponse
from .attendance import AttendanceCreate, AttendanceUpdate, AttendanceResponse
from .leave import LeaveCreate, LeaveUpdate, LeaveResponse
from .shift import ShiftCreate, ShiftUpdate, ShiftResponse
from .schedule import ScheduleCreate, ScheduleUpdate, ScheduleResponse
from .payroll import PayrollCreate, PayrollUpdate, PayrollResponse
from .event import EventCreate, EventUpdate, EventResponse
from .notification import NotificationCreate, NotificationUpdate, NotificationResponse
from .message import MessageCreate, MessageUpdate, MessageResponse
from .chat import ChatCreate, ChatResponse
from .complaint import ComplaintCreate, ComplaintUpdate, ComplaintResponse
from .feedback import FeedbackCreate, FeedbackUpdate, FeedbackResponse
from .faq import FAQCreate, FAQUpdate, FAQResponse
from .setting import SettingCreate, SettingUpdate, SettingResponse
from .role import RoleCreate, RoleUpdate, RoleResponse
from .role_permission import RolePermissionCreate, RolePermissionResponse
from .api_key import APIKeyCreate, APIKeyResponse
from .audit_log import AuditLogResponse
from .activity_log import ActivityLogResponse

__all__ = [
    # Base
    "ResponseModel",
    "PaginatedResponse",
    "StatusResponse",
    
    # User & Auth
    "UserCreate", "UserUpdate", "UserResponse", "UserLogin", "TokenResponse",
    
    # Infrastructure
    "FloorCreate", "FloorUpdate", "FloorResponse", "FloorListResponse", "FloorDetailResponse",
    "HospitalCreate", "HospitalUpdate", "HospitalResponse", "HospitalDetailResponse",
    "BranchCreate", "BranchUpdate", "BranchResponse",
    "DepartmentCreate", "DepartmentUpdate", "DepartmentResponse", "DepartmentDetailResponse",
    "WardCreate", "WardUpdate", "WardResponse", "WardDetailResponse",
    "RoomCreate", "RoomUpdate", "RoomResponse", "RoomDetailResponse",
    "BedCreate", "BedUpdate", "BedResponse", "BedAssignment",
    
    # People
    "PatientCreate", "PatientUpdate", "PatientResponse", "PatientDetailResponse",
    "DoctorCreate", "DoctorUpdate", "DoctorResponse", "DoctorDetailResponse",
    "NurseCreate", "NurseUpdate", "NurseResponse",
    "StaffCreate", "StaffUpdate", "StaffResponse",
    
    # Medical Services
    "AppointmentCreate", "AppointmentUpdate", "AppointmentResponse", "AppointmentDetailResponse",
    "AdmissionCreate", "AdmissionUpdate", "AdmissionResponse", "AdmissionDetailResponse",
    "DischargeCreate", "DischargeUpdate", "DischargeResponse",
    "LabTestCreate", "LabTestUpdate", "LabTestResponse",
    "LabReportCreate", "LabReportUpdate", "LabReportResponse",
    "MedicineCreate", "MedicineUpdate", "MedicineResponse",
    "PrescriptionCreate", "PrescriptionUpdate", "PrescriptionResponse",
    "PharmacyCreate", "PharmacyUpdate", "PharmacyResponse",
    
    # Emergency & Imaging
    "EmergencyCreate", "EmergencyUpdate", "EmergencyResponse",
    "AmbulanceCreate", "AmbulanceUpdate", "AmbulanceResponse",
    "OperationCreate", "OperationUpdate", "OperationResponse",
    "ImagingCreate", "ImagingUpdate", "ImagingResponse",
    
    # Financial
    "BillingCreate", "BillingUpdate", "BillingResponse", "BillingDetailResponse",
    "PaymentCreate", "PaymentUpdate", "PaymentResponse",
    "InsuranceCreate", "InsuranceUpdate", "InsuranceResponse",
    "ExpenseCreate", "ExpenseUpdate", "ExpenseResponse",
    "RevenueCreate", "RevenueUpdate", "RevenueResponse",
    
    # Resources
    "EquipmentCreate", "EquipmentUpdate", "EquipmentResponse",
    "InventoryCreate", "InventoryUpdate", "InventoryResponse",
    "SupplierCreate", "SupplierUpdate", "SupplierResponse",
    "VendorCreate", "VendorUpdate", "VendorResponse",
    "PurchaseOrderCreate", "PurchaseOrderUpdate", "PurchaseOrderResponse",
    
    # HR
    "AttendanceCreate", "AttendanceUpdate", "AttendanceResponse",
    "LeaveCreate", "LeaveUpdate", "LeaveResponse",
    "ShiftCreate", "ShiftUpdate", "ShiftResponse",
    "ScheduleCreate", "ScheduleUpdate", "ScheduleResponse",
    "PayrollCreate", "PayrollUpdate", "PayrollResponse",
    
    # Communication
    "EventCreate", "EventUpdate", "EventResponse",
    "NotificationCreate", "NotificationUpdate", "NotificationResponse",
    "MessageCreate", "MessageUpdate", "MessageResponse",
    "ChatCreate", "ChatResponse",
    "ComplaintCreate", "ComplaintUpdate", "ComplaintResponse",
    "FeedbackCreate", "FeedbackUpdate", "FeedbackResponse",
    "FAQCreate", "FAQUpdate", "FAQResponse",
    
    # System
    "SettingCreate", "SettingUpdate", "SettingResponse",
    "RoleCreate", "RoleUpdate", "RoleResponse",
    "RolePermissionCreate", "RolePermissionResponse",
    "APIKeyCreate", "APIKeyResponse",
    "AuditLogResponse",
    "ActivityLogResponse",
]
