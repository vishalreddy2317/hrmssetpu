# app/services/permission_service.py

from app.schemas.helpers import (
    get_template_permissions,
    get_available_templates,
    PERMISSION_TEMPLATES
)
from app.models.role import Role
from app.models.role_permission import RolePermission
from sqlalchemy.orm import Session


class PermissionService:
    
    @staticmethod
    def create_role_from_template(
        db: Session,
        role_name: str,
        template_name: str
    ) -> Role:
        """Create a role with permissions from template"""
        
        # Get template permissions
        template_perms = get_template_permissions(template_name)
        
        if not template_perms:
            raise ValueError(f"Template '{template_name}' not found")
        
        # Create role
        role = Role(
            name=role_name,
            code=template_name,
            role_type="custom",
            is_default_for=template_name.lower() if template_name in ["DOCTOR", "NURSE", "PATIENT"] else None
        )
        db.add(role)
        db.flush()
        
        # Add permissions
        for perm in template_perms:
            role_permission = RolePermission(
                role_id=role.id,
                resource=perm["resource"],
                action=perm["action"],
                permission_code=f"{perm['resource']}:{perm['action']}",
                is_granted=True
            )
            db.add(role_permission)
        
        db.commit()
        db.refresh(role)
        
        return role
    
    @staticmethod
    def get_available_templates() -> list:
        """Get all available permission templates"""
        return get_available_templates()