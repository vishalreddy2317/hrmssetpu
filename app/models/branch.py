"""
Branch Model
Hospital branch locations
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index, CheckConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional, List

from .base import BaseModel


class Branch(BaseModel):
    """
    Hospital branch model
    Manages multiple locations of the same hospital
    """
    
    __tablename__ = "branches"
    
    # Basic Information
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    
    # Hospital Reference
    hospital_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("hospitals.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Location
    address: Mapped[str] = mapped_column(Text, nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), default="USA")
    pincode: Mapped[str] = mapped_column(String(20), nullable=False)
    
    # Contact
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    email: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Building Details
    total_floors: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    basement_floors: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Capacity
    total_beds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_rooms: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default='active', index=True)
    is_main_branch: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Additional Info
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationships
    hospital: Mapped["Hospital"] = relationship(
        "Hospital",
        back_populates="branches"
    )
    
    floors: Mapped[List["Floor"]] = relationship(
        "Floor",
        back_populates="branch",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    departments: Mapped[List["Department"]] = relationship(
        "Department",
        back_populates="branch",
        lazy="dynamic"
    )
    
    # Table Arguments
    __table_args__ = (
        CheckConstraint('total_floors >= 1', name='branch_min_one_floor'),
        Index('idx_branch_hospital', 'hospital_id', 'status'),
        {'comment': 'Hospital branch locations'}
    )
    
    def __repr__(self) -> str:
        return f"<Branch(id={self.id}, name='{self.name}', code='{self.code}')>"
    
