"""
Base models and mixins for SQLAlchemy 2.0
Provides common fields and functionality for all models
"""

from datetime import datetime
from typing import Any
from sqlalchemy import Column, Integer, DateTime, Boolean, func, event
from sqlalchemy.orm import declared_attr, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base


# ============================================
# Mixins
# ============================================

class TimestampMixin:
    """Mixin for created_at and updated_at timestamps"""
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


class SoftDeleteMixin:
    """Mixin for soft delete functionality"""
    
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
    def soft_delete(self) -> None:
        """Mark record as deleted"""
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()
    
    def restore(self) -> None:
        """Restore soft-deleted record"""
        self.is_deleted = False
        self.deleted_at = None


class ActiveMixin:
    """Mixin for is_active flag"""
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    
    def activate(self) -> None:
        """Activate record"""
        self.is_active = True
    
    def deactivate(self) -> None:
        """Deactivate record"""
        self.is_active = False


# ============================================
# Base Model
# ============================================

class BaseModel(TimestampMixin, SoftDeleteMixin, ActiveMixin):
    """
    Base model with common fields for all models
    Includes: id, timestamps, soft delete, active flag
    """
    
    __abstract__ = True
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    
    @declared_attr
    def __tablename__(cls) -> str:
        """Generate table name from class name"""
        return cls.__name__.lower() + 's'
    
    def to_dict(self) -> dict[str, Any]:
        """
        Convert model to dictionary
        
        Returns:
            Dictionary representation of model
        """
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def update(self, **kwargs) -> None:
        """
        Update model attributes
        
        Args:
            **kwargs: Attributes to update
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def __repr__(self) -> str:
        """String representation"""
        attrs = ", ".join(
            f"{col.name}={getattr(self, col.name)!r}"
            for col in self.__table__.columns
            if col.name in ['id', 'name'] or col.primary_key
        )
        return f"<{self.__class__.__name__}({attrs})>"


# ============================================
# Event Listeners
# ============================================

@event.listens_for(BaseModel, 'before_update', propagate=True)
def receive_before_update(mapper, connection, target):
    """Update timestamp before update"""
    target.updated_at = datetime.utcnow()


@event.listens_for(BaseModel, 'before_insert', propagate=True)
def receive_before_insert(mapper, connection, target):
    """Set timestamps before insert"""
    now = datetime.utcnow()
    target.created_at = now
    target.updated_at = now


# ============================================
# Exports
# ============================================

__all__ = [
    "BaseModel",
    "TimestampMixin",
    "SoftDeleteMixin",
    "ActiveMixin",
]
