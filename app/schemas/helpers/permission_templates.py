"""
Permission Template Definitions
Pre-defined permission sets for common roles
"""

from typing import Dict, List

PERMISSION_TEMPLATES: Dict[str, List[Dict[str, str]]] = {
    "SUPER_ADMIN": [
        {"resource": resource, "action": action}
        for resource in [
            "patients", "appointments", "doctors", "nurses", "staff",
            "billing", "payments", "prescriptions", "lab_tests", "radiology",
            "pharmacy", "inventory", "departments", "wards", "beds",
            "admissions", "discharges", "procedures", "reports", "settings",
            "users", "roles", "permissions", "audit_logs", "notifications"
        ]
        for action in ["create", "read", "update", "delete", "list", "export", "approve", "reject"]
    ],
    
    "ADMIN": [
        {"resource": resource, "action": action}
        for resource in [
            "patients", "appointments", "doctors", "nurses", "staff",
            "billing", "payments", "departments", "wards", "beds",
            "reports", "settings", "users", "notifications"
        ]
        for action in ["create", "read", "update", "delete", "list", "export"]
    ],
    
    "DOCTOR": [
        {"resource": "patients", "action": "read"},
        {"resource": "patients", "action": "list"},
        {"resource": "patients", "action": "update"},
        {"resource": "appointments", "action": "read"},
        {"resource": "appointments", "action": "list"},
        {"resource": "appointments", "action": "update"},
        {"resource": "prescriptions", "action": "create"},
        {"resource": "prescriptions", "action": "read"},
        {"resource": "prescriptions", "action": "update"},
        {"resource": "lab_tests", "action": "create"},
        {"resource": "lab_tests", "action": "read"},
        {"resource": "radiology", "action": "create"},
        {"resource": "radiology", "action": "read"},
        {"resource": "procedures", "action": "create"},
        {"resource": "procedures", "action": "read"},
        {"resource": "procedures", "action": "update"},
        {"resource": "admissions", "action": "create"},
        {"resource": "admissions", "action": "read"},
        {"resource": "discharges", "action": "create"},
        {"resource": "reports", "action": "read"},
    ],
    
    "NURSE": [
        {"resource": "patients", "action": "read"},
        {"resource": "patients", "action": "list"},
        {"resource": "appointments", "action": "read"},
        {"resource": "appointments", "action": "list"},
        {"resource": "prescriptions", "action": "read"},
        {"resource": "lab_tests", "action": "read"},
        {"resource": "radiology", "action": "read"},
        {"resource": "procedures", "action": "read"},
        {"resource": "admissions", "action": "read"},
        {"resource": "admissions", "action": "update"},
        {"resource": "wards", "action": "read"},
        {"resource": "beds", "action": "read"},
        {"resource": "beds", "action": "update"},
    ],
    
    "RECEPTIONIST": [
        {"resource": "patients", "action": "create"},
        {"resource": "patients", "action": "read"},
        {"resource": "patients", "action": "update"},
        {"resource": "patients", "action": "list"},
        {"resource": "appointments", "action": "create"},
        {"resource": "appointments", "action": "read"},
        {"resource": "appointments", "action": "update"},
        {"resource": "appointments", "action": "list"},
        {"resource": "billing", "action": "read"},
        {"resource": "billing", "action": "list"},
        {"resource": "payments", "action": "create"},
        {"resource": "payments", "action": "read"},
    ],
    
    "PHARMACIST": [
        {"resource": "patients", "action": "read"},
        {"resource": "prescriptions", "action": "read"},
        {"resource": "prescriptions", "action": "list"},
        {"resource": "pharmacy", "action": "create"},
        {"resource": "pharmacy", "action": "read"},
        {"resource": "pharmacy", "action": "update"},
        {"resource": "pharmacy", "action": "list"},
        {"resource": "inventory", "action": "read"},
        {"resource": "inventory", "action": "update"},
        {"resource": "inventory", "action": "list"},
    ],
    
    "LAB_TECHNICIAN": [
        {"resource": "patients", "action": "read"},
        {"resource": "lab_tests", "action": "read"},
        {"resource": "lab_tests", "action": "update"},
        {"resource": "lab_tests", "action": "list"},
        {"resource": "reports", "action": "create"},
        {"resource": "reports", "action": "read"},
    ],
    
    "RADIOLOGIST": [
        {"resource": "patients", "action": "read"},
        {"resource": "radiology", "action": "read"},
        {"resource": "radiology", "action": "update"},
        {"resource": "radiology", "action": "list"},
        {"resource": "reports", "action": "create"},
        {"resource": "reports", "action": "read"},
    ],
    
    "PATIENT": [
        {"resource": "appointments", "action": "create"},
        {"resource": "appointments", "action": "read"},
        {"resource": "appointments", "action": "list"},
        {"resource": "prescriptions", "action": "read"},
        {"resource": "lab_tests", "action": "read"},
        {"resource": "radiology", "action": "read"},
        {"resource": "billing", "action": "read"},
        {"resource": "payments", "action": "read"},
        {"resource": "reports", "action": "read"},
    ],
    
    "ACCOUNTANT": [
        {"resource": "billing", "action": "create"},
        {"resource": "billing", "action": "read"},
        {"resource": "billing", "action": "update"},
        {"resource": "billing", "action": "list"},
        {"resource": "billing", "action": "export"},
        {"resource": "payments", "action": "create"},
        {"resource": "payments", "action": "read"},
        {"resource": "payments", "action": "update"},
        {"resource": "payments", "action": "list"},
        {"resource": "payments", "action": "export"},
        {"resource": "reports", "action": "read"},
        {"resource": "reports", "action": "export"},
    ],
}


def get_template_permissions(template_name: str) -> List[Dict[str, str]]:
    """
    Get permissions for a specific template
    
    Args:
        template_name: Name of the template (e.g., 'DOCTOR', 'NURSE')
        
    Returns:
        List of permission dictionaries
    """
    return PERMISSION_TEMPLATES.get(template_name.upper(), [])


def get_available_templates() -> List[str]:
    """
    Get list of available template names
    
    Returns:
        List of template names
    """
    return list(PERMISSION_TEMPLATES.keys())


def get_template_info() -> Dict[str, Dict]:
    """
    Get detailed information about all templates
    
    Returns:
        Dictionary with template names and their details
    """
    return {
        name: {
            "permission_count": len(perms),
            "resources": list(set(p["resource"] for p in perms)),
            "actions": list(set(p["action"] for p in perms)),
        }
        for name, perms in PERMISSION_TEMPLATES.items()
    }


def create_custom_template(
    template_name: str,
    base_template: str,
    additional_permissions: List[Dict[str, str]] = None,
    remove_permissions: List[Dict[str, str]] = None
) -> List[Dict[str, str]]:
    """
    Create a custom template based on an existing one
    
    Args:
        template_name: Name for the new template
        base_template: Existing template to base on
        additional_permissions: Permissions to add
        remove_permissions: Permissions to remove
        
    Returns:
        List of permissions for the new template
    """
    base_perms = get_template_permissions(base_template)
    
    if not base_perms:
        raise ValueError(f"Base template '{base_template}' not found")
    
    # Start with base permissions
    new_perms = base_perms.copy()
    
    # Add additional permissions
    if additional_permissions:
        new_perms.extend(additional_permissions)
    
    # Remove specified permissions
    if remove_permissions:
        for perm in remove_permissions:
            if perm in new_perms:
                new_perms.remove(perm)
    
    # Remove duplicates
    unique_perms = []
    seen = set()
    for perm in new_perms:
        perm_tuple = (perm["resource"], perm["action"])
        if perm_tuple not in seen:
            seen.add(perm_tuple)
            unique_perms.append(perm)
    
    return unique_perms