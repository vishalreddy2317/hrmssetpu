"""
Department Model - Updated with Floor Reference
Hospital departments with floor location
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional, List

from .base import BaseModel


class Department(BaseModel):
    """
    Department model with floor reference
    Manages hospital departments across different floors
    """
    
    __tablename__ = "departments"
    
    # Basic Information
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    
    # Department Type
    department_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        comment="clinical, diagnostic, support, administrative"
    )
    
    # ⭐ Floor Reference - NEW
    main_floor_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("floors.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    main_floor_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)
    
    # Location
    hospital_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("hospitals.id", ondelete="CASCADE"),
        index=True
    )
    branch_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("branches.id", ondelete="CASCADE"),
        index=True
    )
    building: Mapped[Optional[str]] = mapped_column(String(50))
    wing: Mapped[Optional[str]] = mapped_column(String(50), comment="East, West, North, South")
    
    # Management
    head_doctor_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("doctors.id", ondelete="SET NULL")
    )
    
    # Contact
    contact_number: Mapped[Optional[str]] = mapped_column(String(20))
    email: Mapped[Optional[str]] = mapped_column(String(100))
    extension: Mapped[Optional[str]] = mapped_column(String(10))
    
    # Staff Count
    total_doctors: Mapped[int] = mapped_column(Integer, default=0)
    total_nurses: Mapped[int] = mapped_column(Integer, default=0)
    total_staff: Mapped[int] = mapped_column(Integer, default=0)
    
    # Facilities
    total_rooms: Mapped[int] = mapped_column(Integer, default=0)
    total_beds: Mapped[int] = mapped_column(Integer, default=0)
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default='active', index=True)
    is_emergency_department: Mapped[bool] = mapped_column(Boolean, default=False)
    is_24x7: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Additional Info
    description: Mapped[Optional[str]] = mapped_column(Text)
    services_offered: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationships
    main_floor: Mapped[Optional["Floor"]] = relationship(
        "Floor",
        back_populates="departments",
        foreign_keys=[main_floor_id]
    )
    
    hospital: Mapped[Optional["Hospital"]] = relationship(
        "Hospital",
        back_populates="departments"
    )
    
    branch: Mapped[Optional["Branch"]] = relationship(
        "Branch",
        back_populates="departments"
    )
    
    head_doctor: Mapped[Optional["Doctor"]] = relationship(
        "Doctor",
        back_populates="departments_managed",
        foreign_keys=[head_doctor_id]
    )
    
    doctors: Mapped[List["Doctor"]] = relationship(
        "Doctor",
        back_populates="department",
        foreign_keys="Doctor.department_id",
        lazy="dynamic"
    )
    
    nurses: Mapped[List["Nurse"]] = relationship(
        "Nurse",
        back_populates="department",
        lazy="dynamic"
    )
    
    rooms: Mapped[List["Room"]] = relationship(
        "Room",
        back_populates="department",
        lazy="dynamic"
    )
    
    wards: Mapped[List["Ward"]] = relationship(
        "Ward",
        back_populates="department",
        lazy="dynamic"
    )
    
    appointments: Mapped[List["Appointment"]] = relationship(
        "Appointment",
        back_populates="department",
        lazy="dynamic"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('total_doctors >= 0', name='dept_positive_doctors'),
        CheckConstraint('total_nurses >= 0', name='dept_positive_nurses'),
        Index('idx_department_floor', 'main_floor_id', 'main_floor_number'),
        Index('idx_department_hospital', 'hospital_id', 'status'),
        Index('idx_department_type', 'department_type', 'status'),
        {'comment': 'Hospital departments with floor locations'}
    )
    
    # Validators
    @validates('department_type')
    def validate_department_type(self, key, value):
        """Validate department type"""
        valid_types = [
            'clinical', 'diagnostic', 'support', 'administrative',
            'emergency', 'surgical', 'medical', 'pediatric'
        ]
        if value.lower() not in valid_types:
            raise ValueError(f"Department type must be one of: {', '.join(valid_types)}")
        return value.lower()
    
    def __repr__(self) -> str:
        floor_info = f", floor={self.main_floor_number}" if self.main_floor_number is not None else ""
        return f"<Department(id={self.id}, name='{self.name}'{floor_info})>"
