"""
Role Permission Model
Role-based permissions mapping
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Optional

from .base import BaseModel


class RolePermission(BaseModel):
    """
    Role permission mapping model
    """
    
    __tablename__ = "role_permissions"
    
    # Role
    role_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("roles.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Permission Details
    resource: Mapped[str] = mapped_column(String(100), nullable=False, index=True, comment="patients, appointments, billing, etc.")
    action: Mapped[str] = mapped_column(String(50), nullable=False, comment="create, read, update, delete, list")
    
    # Permission Code (composite)
    permission_code: Mapped[str] = mapped_column(String(200), nullable=False, index=True, comment="resource:action e.g., patients:create")
    
    # Granted
    is_granted: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Conditions (optional)
    conditions: Mapped[Optional[str]] = mapped_column(String(500), comment="JSON conditions for permission")
    
    # Relationships
    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="role_permissions"
    )
    
    # Table Arguments
    __table_args__ = (
        UniqueConstraint('role_id', 'permission_code', name='unique_role_permission'),
        Index('idx_rolepermission_role', 'role_id', 'resource'),
        Index('idx_rolepermission_code', 'permission_code', 'is_granted'),
        {'comment': 'Role-based permissions mapping'}
    )
    
    # Validators
    @validates('action')
    def validate_action(self, key, value):
        valid_actions = ['create', 'read', 'update', 'delete', 'list', 'export', 'approve', 'reject']
        if value.lower() not in valid_actions:
            raise ValueError(f"Action must be one of: {', '.join(valid_actions)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<RolePermission(role_id={self.role_id}, permission='{self.permission_code}')>"