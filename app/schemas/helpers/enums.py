"""
Enum definitions for type safety
"""

from enum import Enum


class UserType(str, Enum):
    PATIENT = "patient"
    DOCTOR = "doctor"
    NURSE = "nurse"
    STAFF = "staff"
    ADMIN = "admin"
    RECEPTIONIST = "receptionist"
    PHARMACIST = "pharmacist"
    LAB_TECHNICIAN = "lab_technician"
    RADIOLOGIST = "radiologist"


class PaymentMethod(str, Enum):
    CASH = "cash"
    CARD = "card"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    UPI = "upi"
    NET_BANKING = "net_banking"
    CHEQUE = "cheque"
    INSURANCE = "insurance"
    ONLINE = "online"
    MOBILE_PAYMENT = "mobile_payment"


class AppointmentStatus(str, Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    CHECKED_IN = "checked_in"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"
    RESCHEDULED = "rescheduled"


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class BloodGroup(str, Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"
    UNKNOWN = "unknown"


class PriorityLevel(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"
    EMERGENCY = "emergency"


class RevenueSource(str, Enum):
    CONSULTATIONS = "consultations"
    PROCEDURES = "procedures"
    PHARMACY = "pharmacy"
    LAB = "lab"
    IMAGING = "imaging"
    ROOM_CHARGES = "room_charges"
    EMERGENCY = "emergency"
    SURGERY = "surgery"
    MISCELLANEOUS = "miscellaneous"
    INSURANCE = "insurance"


class PermissionAction(str, Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    LIST = "list"
    EXPORT = "export"
    APPROVE = "approve"
    REJECT = "reject"
    VIEW = "view"