"""
Role Model
User roles and access control
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, Index
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional, List

from .base import BaseModel


class Role(BaseModel):
    """
    User role model
    """
    
    __tablename__ = "roles"
    
    # Role Details
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    
    # Description
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    # Role Type
    role_type: Mapped[str] = mapped_column(
        String(50),
        default='custom',
        nullable=False,
        comment="system, custom"
    )
    
    # Level (hierarchy)
    level: Mapped[int] = mapped_column(Integer, default=0, comment="Higher number = more privileges")
    
    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default='active',
        nullable=False,
        index=True,
        comment="active, inactive"
    )
    
    # Permissions Summary
    permissions: Mapped[Optional[str]] = mapped_column(Text, comment="JSON array of permission codes")
    
    # Default for User Type
    is_default_for: Mapped[Optional[str]] = mapped_column(String(50), comment="doctor, nurse, patient, staff, admin")
    
    # Relationships
    role_permissions: Mapped[List["RolePermission"]] = relationship(
        "RolePermission",
        back_populates="role",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    # Table Arguments
    __table_args__ = (
        Index('idx_role_type', 'role_type', 'status'),
        {'comment': 'User roles and access control'}
    )
    
    # Validators
    @validates('role_type')
    def validate_role_type(self, key, value):
        valid_types = ['system', 'custom']
        if value.lower() not in valid_types:
            raise ValueError(f"Role type must be one of: {', '.join(valid_types)}")
        return value.lower()
    
    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['active', 'inactive']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<Role(id={self.id}, name='{self.name}', code='{self.code}')>"