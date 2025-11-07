"""
Setting Model
System configuration and settings
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, Index
from sqlalchemy.orm import Mapped, mapped_column, validates
from typing import Optional

from .base import BaseModel


class Setting(BaseModel):
    """
    System settings model
    """
    
    __tablename__ = "settings"
    
    # Setting Key
    setting_key: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    
    # Setting Value
    setting_value: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Data Type
    data_type: Mapped[str] = mapped_column(
        String(20),
        default='string',
        nullable=False,
        comment="string, integer, boolean, json, float"
    )
    
    # Category
    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        comment="general, email, sms, payment, notification, security, appearance"
    )
    
    # Description
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    # Is Sensitive (passwords, API keys, etc.)
    is_sensitive: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Is Editable
    is_editable: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Default Value
    default_value: Mapped[Optional[str]] = mapped_column(Text)
    
    # Validation Rules
    validation_rules: Mapped[Optional[str]] = mapped_column(Text, comment="JSON format")
    
    # Last Modified By
    modified_by: Mapped[Optional[str]] = mapped_column(String(200))
    
    # Table Arguments
    __table_args__ = (
        Index('idx_setting_category', 'category'),
        {'comment': 'System configuration and settings'}
    )
    
    # Validators
    @validates('data_type')
    def validate_data_type(self, key, value):
        valid_types = ['string', 'integer', 'boolean', 'json', 'float', 'array']
        if value.lower() not in valid_types:
            raise ValueError(f"Data type must be one of: {', '.join(valid_types)}")
        return value.lower()
    
    @validates('category')
    def validate_category(self, key, value):
        valid_categories = [
            'general', 'email', 'sms', 'payment', 'notification',
            'security', 'appearance', 'appointment', 'billing', 'system'
        ]
        if value.lower() not in valid_categories:
            raise ValueError(f"Category must be one of: {', '.join(valid_categories)}")
        return value.lower()
    
    def __repr__(self) -> str:
        return f"<Setting(key='{self.setting_key}', category='{self.category}')>"