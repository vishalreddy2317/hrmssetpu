# app/api/v1/endpoints/roles.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.role_schema import RoleCreate, RoleResponse
from app.schemas.helpers import get_available_templates
from app.services.permission_service import PermissionService

router = APIRouter()


@router.get("/templates")
def get_permission_templates():
    """Get available permission templates"""
    templates = get_available_templates()
    return {
        "templates": templates,
        "total": len(templates)
    }


@router.post("/from-template")
def create_role_from_template(
    role_name: str,
    template_name: str,
    db: Session = Depends(get_db)
):
    """Create role from permission template"""
    try:
        role = PermissionService.create_role_from_template(
            db=db,
            role_name=role_name,
            template_name=template_name
        )
        return {
            "message": f"Role '{role_name}' created from template '{template_name}'",
            "role": role
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))