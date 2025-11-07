"""
Complaint Model
Patient and staff complaints/grievances
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional

from .base import BaseModel


class Complaint(BaseModel):
    """
    Complaint/Grievance model
    """
    
    __tablename__ = "complaints"
    
    # Complaint Details
    complaint_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Complainant
    complainant_name: Mapped[str] = mapped_column(String(200), nullable=False)
    complainant_email: Mapped[Optional[str]] = mapped_column(String(100))
    complainant_phone: Mapped[str] = mapped_column(String(20), nullable=False)
    complainant_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="patient, visitor, staff, doctor, vendor"
    )
    
    # Patient Reference (if applicable)
    patient_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("patients.id", ondelete="SET NULL"),
        index=True
    )
    
    # Category
    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        comment="medical_care, staff_behavior, facility, billing, administration, hygiene, food"
    )
    
    # Department
    department_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("departments.id", ondelete="SET NULL")
    )
    
    # Severity
    severity: Mapped[str] = mapped_column(
        String(20),
        default='medium',
        nullable=False,
        comment="low, medium, high, critical"
    )
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='open',
        nullable=False,
        index=True,
        comment="open, in_progress, resolved, closed, rejected"
    )
    
    # Dates
    incident_date: Mapped[Optional[str]] = mapped_column(String(20))
    filed_date: Mapped[str] = mapped_column(String(20), nullable=False)
    
    # Assignment
    assigned_to: Mapped[Optional[str]] = mapped_column(String(200))
    assigned_date: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Resolution
    resolution: Mapped[Optional[str]] = mapped_column(Text)
    resolved_by: Mapped[Optional[str]] = mapped_column(String(200))
    resolved_date: Mapped[Optional[str]] = mapped_column(String(20))
    resolution_time_hours: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Follow-up
    requires_followup: Mapped[bool] = mapped_column(Boolean, default=False)
    followup_date: Mapped[Optional[str]] = mapped_column(String(20))
    followup_notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Satisfaction
    is_satisfied: Mapped[Optional[bool]] = mapped_column(Boolean)
    satisfaction_rating: Mapped[Optional[int]] = mapped_column(Integer)
    satisfaction_comments: Mapped[Optional[str]] = mapped_column(Text)
    
    # Attachments
    attachments: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array of attachment URLs")
    
    # Notes
    notes: Mapped[Optional[str]] = mapped_column(Text)
    internal_notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationships
    patient: Mapped[Optional["Patient"]] = relationship(
        "Patient",
        backref="complaints"
    )
    
    department: Mapped[Optional["Department"]] = relationship(
        "Department",
        backref="complaints"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('satisfaction_rating >= 1 AND satisfaction_rating <= 5 OR satisfaction_rating IS NULL', name='complaint_valid_rating'),
        Index('idx_complaint_category', 'category', 'status'),
        Index('idx_complaint_status', 'status', 'severity'),
        Index('idx_complaint_filed_date', 'filed_date', 'status'),
        {'comment': 'Patient and staff complaints/grievances'}
    )
    
    # Validators
    @validates('category')
    def validate_category(self, key, value):
        valid_categories = [
            'medical_care', 'staff_behavior', 'facility', 'billing',
            'administration', 'hygiene', 'food', 'waiting_time', 'communication'
        ]
        if value.lower() not in valid_categories:
            raise ValueError(f"Category must be one of: {', '.join(valid_categories)}")
        return value.lower()
    
    @validates('severity')
    def validate_severity(self, key, value):
        valid_severities = ['low', 'medium', 'high', 'critical']
        if value.lower() not in valid_severities:
            raise ValueError(f"Severity must be one of: {', '.join(valid_severities)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['open', 'in_progress', 'resolved', 'closed', 'rejected']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<Complaint(id={self.id}, number='{self.complaint_number}', status='{self.status}')>"