"""
Feedback Model
Patient and service feedback
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional

from .base import BaseModel


class Feedback(BaseModel):
    """
    Feedback model
    """
    
    __tablename__ = "feedbacks"
    
    # Feedback Details
    feedback_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    
    # Patient
    patient_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("patients.id", ondelete="SET NULL"),
        index=True
    )
    patient_name: Mapped[Optional[str]] = mapped_column(String(200))
    
    # Contact
    email: Mapped[Optional[str]] = mapped_column(String(100))
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Related Service
    service_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        comment="consultation, admission, emergency, lab, pharmacy, overall"
    )
    
    # Doctor/Staff (if applicable)
    doctor_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("doctors.id", ondelete="SET NULL")
    )
    
    # Department
    department_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("departments.id", ondelete="SET NULL")
    )
    
    # Ratings (1-5 scale)
    overall_rating: Mapped[int] = mapped_column(Integer, nullable=False)
    staff_behavior_rating: Mapped[Optional[int]] = mapped_column(Integer)
    cleanliness_rating: Mapped[Optional[int]] = mapped_column(Integer)
    facilities_rating: Mapped[Optional[int]] = mapped_column(Integer)
    waiting_time_rating: Mapped[Optional[int]] = mapped_column(Integer)
    treatment_quality_rating: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Comments
    positive_comments: Mapped[Optional[str]] = mapped_column(Text)
    negative_comments: Mapped[Optional[str]] = mapped_column(Text)
    suggestions: Mapped[Optional[str]] = mapped_column(Text)
    
    # Experience
    would_recommend: Mapped[Optional[bool]] = mapped_column(Boolean)
    
    # Feedback Date
    feedback_date: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    visit_date: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='received',
        nullable=False,
        comment="received, reviewed, responded, archived"
    )
    
    # Response
    response: Mapped[Optional[str]] = mapped_column(Text)
    responded_by: Mapped[Optional[str]] = mapped_column(String(200))
    response_date: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Public Display
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Source
    source: Mapped[str] = mapped_column(
        String(50),
        default='website',
        nullable=False,
        comment="website, app, email, survey, phone, sms"
    )
    
    # Relationships
    patient: Mapped[Optional["Patient"]] = relationship(
        "Patient",
        backref="feedbacks"
    )
    
    doctor: Mapped[Optional["Doctor"]] = relationship(
        "Doctor",
        backref="feedbacks"
    )
    
    department: Mapped[Optional["Department"]] = relationship(
        "Department",
        backref="feedbacks"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('overall_rating >= 1 AND overall_rating <= 5', name='feedback_valid_overall_rating'),
        CheckConstraint('staff_behavior_rating >= 1 AND staff_behavior_rating <= 5 OR staff_behavior_rating IS NULL', name='feedback_valid_staff_rating'),
        CheckConstraint('cleanliness_rating >= 1 AND cleanliness_rating <= 5 OR cleanliness_rating IS NULL', name='feedback_valid_cleanliness_rating'),
        CheckConstraint('facilities_rating >= 1 AND facilities_rating <= 5 OR facilities_rating IS NULL', name='feedback_valid_facilities_rating'),
        Index('idx_feedback_patient', 'patient_id', 'feedback_date'),
        Index('idx_feedback_service', 'service_type', 'overall_rating'),
        Index('idx_feedback_doctor', 'doctor_id', 'overall_rating'),
        {'comment': 'Patient and service feedback'}
    )
    
    # Validators
    @validates('service_type')
    def validate_service_type(self, key, value):
        valid_types = [
            'consultation', 'admission', 'emergency', 'lab',
            'pharmacy', 'overall', 'surgery', 'nursing_care'
        ]
        if value.lower() not in valid_types:
            raise ValueError(f"Service type must be one of: {', '.join(valid_types)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['received', 'reviewed', 'responded', 'archived']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<Feedback(id={self.id}, rating={self.overall_rating}, service='{self.service_type}')>"