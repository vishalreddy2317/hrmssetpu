# app/core/seed.py

from sqlalchemy.orm import Session
from app.models.role import Role
from app.models.role_permission import RolePermission
from app.schemas.helpers import PERMISSION_TEMPLATES


def seed_roles_and_permissions(db: Session):
    """Seed default roles with permissions from templates"""
    
    for template_name, permissions in PERMISSION_TEMPLATES.items():
        # Check if role exists
        existing_role = db.query(Role).filter(
            Role.code == template_name
        ).first()
        
        if existing_role:
            print(f"Role {template_name} already exists, skipping...")
            continue
        
        # Create role
        role = Role(
            name=template_name.replace('_', ' ').title(),
            code=template_name,
            role_type="system",
            level=100 if template_name == "SUPER_ADMIN" else 50,
            status="active"
        )
        db.add(role)
        db.flush()
        
        # Add permissions
        for perm in permissions:
            role_permission = RolePermission(
                role_id=role.id,
                resource=perm["resource"],
                action=perm["action"],
                permission_code=f"{perm['resource']}:{perm['action']}",
                is_granted=True
            )
            db.add(role_permission)
        
        print(f"Created role: {template_name} with {len(permissions)} permissions")
    
    db.commit()
    print("✅ Roles and permissions seeded successfully!")


if __name__ == "__main__":
    from app.core.database import SessionLocal
    db = SessionLocal()
    try:
        seed_roles_and_permissions(db)
    finally:
        db.close()