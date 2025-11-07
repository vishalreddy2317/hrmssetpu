# app/main.py
import os
import logging
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_db, init_db
from app.auth.utils import verify_token
from app.auth.models import User
from app.core.config import settings  # 🧠 You’ll create this (see below)

# Routers
from app.auth.routes import router as auth_router
from app.routers import (
    activity_log_router, ambulance_router, api_key_router, appointment_router,
    attendance_router, audit_log_router, base_router, bed_router, billing_router,
    chat_router, complaint_router, department_router, diagnosis_router, doctor_router,
    event_router, faq_router, feedback_router, imaging_router, insurance_router,
    inventory_router, lab_report_router, lab_test_router, leave_router, medical_record_router,
    medicine_router, message_router, notification_router, nurse_router, patient_router,
    payment_router, payroll_router, pharmacy_router, prescription_router, procedure_router,
    purchase_order_router, radiology_router, role_router, role_permission_router,
    schedule_router, setting_router, shift_router, stock_router, supplier_router,
    transport_router, user_router, vendor_router, ward_router
)

# ============================================================
# 🔹 Logging Configuration
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# ============================================================
# 🔹 App Initialization
# ============================================================

app = FastAPI(
    title="🏥 Hospital SaaS API",
    description="A full-featured hospital management system with JWT & 2FA.",
    version="1.0.0",
)

# ============================================================
# 🔹 Environment-Based CORS
# ============================================================

origins = (
    ["http://localhost:3000", "http://127.0.0.1:5173"]
    if settings.ENVIRONMENT == "development"
    else [settings.FRONTEND_URL]  # Example: "https://hospitalapp.in"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# 🔹 JWT Authentication Dependency
# ============================================================

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    token = credentials.credentials
    try:
        payload = verify_token(token)
    except Exception as e:
        logger.warning(f"Token verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )

    user_id = int(payload.get("sub"))
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user

# ============================================================
# 🔹 Error Handling Middleware
# ============================================================

@app.middleware("http")
async def global_error_handler(request: Request, call_next):
    try:
        return await call_next(request)
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail},
        )
    except Exception as e:
        logger.exception("Unhandled error:")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"},
        )

# ============================================================
# 🔹 Include Routers
# ============================================================

routers = [
    auth_router, activity_log_router, ambulance_router, api_key_router, appointment_router,
    attendance_router, audit_log_router, base_router, bed_router, billing_router, chat_router,
    complaint_router, department_router, diagnosis_router, doctor_router, event_router,
    faq_router, feedback_router, imaging_router, insurance_router, inventory_router,
    lab_report_router, lab_test_router, leave_router, medical_record_router, medicine_router,
    message_router, notification_router, nurse_router, patient_router, payment_router,
    payroll_router, pharmacy_router, prescription_router, procedure_router, purchase_order_router,
    radiology_router, role_router, role_permission_router, schedule_router, setting_router,
    shift_router, stock_router, supplier_router, transport_router, user_router, vendor_router, ward_router
]

for router in routers:
    app.include_router(router)

# ============================================================
# 🔹 Startup Event
# ============================================================

@app.on_event("startup")
async def on_startup():
    logger.info("🚀 Starting Hospital SaaS API...")
    try:
        await init_db()
        logger.info("✅ Database initialized successfully.")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")

# ============================================================
# 🔹 Core Routes
# ============================================================

@app.get("/", tags=["System"])
async def root():
    return {"message": "🚀 Hospital SaaS Backend is running!"}

@app.get("/health", tags=["System"])
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {"status": "ok", "environment": settings.ENVIRONMENT}

@app.get("/protected", tags=["Auth"], summary="Protected route example")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {
        "message": "You have access to this protected route!",
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "phone": current_user.phone,
            "role": current_user.role,
            "is_verified": current_user.is_verified,
        },
    }
