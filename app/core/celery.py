"""
Celery configuration for background tasks
Handles async jobs, scheduled tasks, and email notifications
"""

from celery import Celery
from celery.schedules import crontab
import logging

from .config import settings


# Configure logging
logger = logging.getLogger(__name__)


# ============================================
# Initialize Celery App
# ============================================

celery_app = Celery(
    "hospital_management",
    broker=settings.celery.broker_url,
    backend=settings.celery.result_backend,
    include=[
        "app.services.email",
        "app.services.notification",
        "app.services.backup",
    ]
)


# ============================================
# Celery Configuration
# ============================================

celery_app.conf.update(
    # Serialization
    task_serializer=settings.celery.task_serializer,
    result_serializer=settings.celery.result_serializer,
    accept_content=settings.celery.accept_content,
    
    # Timezone
    timezone=settings.celery.timezone,
    enable_utc=settings.celery.enable_utc,
    
    # Task execution
    task_track_started=settings.celery.task_track_started,
    task_time_limit=settings.celery.task_time_limit,
    task_soft_time_limit=settings.celery.task_soft_time_limit,
    
    # Results
    result_expires=3600,  # 1 hour
    result_persistent=True,
    
    # Worker
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,
    
    # Routing
    task_routes={
        "app.services.email.*": {"queue": "email"},
        "app.services.notification.*": {"queue": "notifications"},
        "app.services.backup.*": {"queue": "maintenance"},
    },
    
    # Broker settings (Redis)
    broker_connection_retry_on_startup=True,
    broker_connection_retry=True,
    broker_connection_max_retries=10,
    
    # Task result backend settings
    result_backend_transport_options={
        "master_name": "mymaster",
        "visibility_timeout": 3600,
    },
)


# ============================================
# Periodic Tasks (Celery Beat)
# ============================================

celery_app.conf.beat_schedule = {
    # Daily database backup at 2 AM
    "daily-database-backup": {
        "task": "app.services.backup.backup_database_task",
        "schedule": crontab(hour=2, minute=0),
        "options": {"queue": "maintenance"},
    },
    
    # Cleanup expired tokens every hour
    "cleanup-expired-tokens": {
        "task": "app.services.auth.cleanup_expired_tokens",
        "schedule": crontab(minute=0),  # Every hour
        "options": {"queue": "maintenance"},
    },
    
    # Send appointment reminders every 15 minutes
    "send-appointment-reminders": {
        "task": "app.services.notification.send_appointment_reminders",
        "schedule": crontab(minute="*/15"),  # Every 15 minutes
        "options": {"queue": "notifications"},
    },
    
    # Check bed availability every 5 minutes
    "check-bed-availability": {
        "task": "app.services.bed.check_bed_availability",
        "schedule": crontab(minute="*/5"),  # Every 5 minutes
        "options": {"queue": "default"},
    },
    
    # Generate daily reports at 6 AM
    "generate-daily-reports": {
        "task": "app.services.reports.generate_daily_report",
        "schedule": crontab(hour=6, minute=0),
        "options": {"queue": "reports"},
    },
    
    # Vacuum database every Sunday at 3 AM
    "vacuum-database": {
        "task": "app.services.maintenance.vacuum_database",
        "schedule": crontab(hour=3, minute=0, day_of_week=0),  # Sunday
        "options": {"queue": "maintenance"},
    },
    
    # Send pending payment reminders daily at 9 AM
    "send-payment-reminders": {
        "task": "app.services.billing.send_payment_reminders",
        "schedule": crontab(hour=9, minute=0),
        "options": {"queue": "notifications"},
    },
    
    # Update patient statistics every 30 minutes
    "update-patient-statistics": {
        "task": "app.services.analytics.update_patient_statistics",
        "schedule": crontab(minute="*/30"),
        "options": {"queue": "analytics"},
    },
}


# ============================================
# Task Base Class
# ============================================

class BaseTask(celery_app.Task):
    """Base task class with error handling"""
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Handle task failure"""
        logger.error(
            f"Task {self.name} failed",
            extra={
                "task_id": task_id,
                "args": args,
                "kwargs": kwargs,
                "error": str(exc),
            },
            exc_info=einfo
        )
    
    def on_success(self, retval, task_id, args, kwargs):
        """Handle task success"""
        logger.info(
            f"Task {self.name} succeeded",
            extra={
                "task_id": task_id,
                "result": str(retval)[:100],  # Truncate long results
            }
        )
    
    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """Handle task retry"""
        logger.warning(
            f"Task {self.name} retrying",
            extra={
                "task_id": task_id,
                "error": str(exc),
            }
        )


# ============================================
# Example Tasks
# ============================================

@celery_app.task(name="send_email", base=BaseTask, bind=True, max_retries=3)
def send_email_task(self, to_email: str, subject: str, body: str):
    """
    Send email task
    
    Args:
        to_email: Recipient email
        subject: Email subject
        body: Email body
    """
    try:
        # Import here to avoid circular imports
        from app.utils.email import send_email
        
        logger.info(f"Sending email to {to_email}")
        send_email(to_email, subject, body)
        logger.info(f"Email sent successfully to {to_email}")
        
        return {"status": "sent", "to": to_email}
        
    except Exception as exc:
        logger.error(f"Failed to send email: {str(exc)}")
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)


@celery_app.task(name="process_payment", base=BaseTask, bind=True)
def process_payment_task(self, payment_id: int):
    """
    Process payment asynchronously
    
    Args:
        payment_id: Payment ID to process
    """
    try:
        logger.info(f"Processing payment {payment_id}")
        
        # Import here to avoid circular imports
        from app.services.billing import process_payment
        
        result = process_payment(payment_id)
        logger.info(f"Payment {payment_id} processed successfully")
        
        return result
        
    except Exception as exc:
        logger.error(f"Payment processing failed: {str(exc)}")
        raise


@celery_app.task(name="generate_report", base=BaseTask)
def generate_report_task(report_type: str, start_date: str, end_date: str):
    """
    Generate report asynchronously
    
    Args:
        report_type: Type of report to generate
        start_date: Start date for report
        end_date: End date for report
    """
    try:
        logger.info(f"Generating {report_type} report")
        
        # Import here to avoid circular imports
        from app.services.reports import generate_report
        
        report_path = generate_report(report_type, start_date, end_date)
        logger.info(f"Report generated: {report_path}")
        
        return {"report_path": report_path, "type": report_type}
        
    except Exception as exc:
        logger.error(f"Report generation failed: {str(exc)}")
        raise


@celery_app.task(name="backup_database", base=BaseTask)
def backup_database_task():
    """
    Backup database task
    """
    try:
        logger.info("Starting database backup")
        
        from app.core.database import backup_database
        from datetime import datetime
        
        backup_path = f"backups/hospital_db_{datetime.now().strftime('%Y%m%d_%H%M%S')}.dump"
        result = backup_database(backup_path)
        
        if result:
            logger.info(f"Database backup completed: {backup_path}")
            return {"status": "success", "path": backup_path}
        else:
            logger.error("Database backup failed")
            return {"status": "failed"}
            
    except Exception as exc:
        logger.error(f"Database backup error: {str(exc)}")
        raise


@celery_app.task(name="send_sms", base=BaseTask, bind=True, max_retries=3)
def send_sms_task(self, phone_number: str, message: str):
    """
    Send SMS notification
    
    Args:
        phone_number: Recipient phone number
        message: SMS message
    """
    try:
        logger.info(f"Sending SMS to {phone_number}")
        
        # Import SMS service
        from app.utils.sms import send_sms
        
        send_sms(phone_number, message)
        logger.info(f"SMS sent successfully to {phone_number}")
        
        return {"status": "sent", "to": phone_number}
        
    except Exception as exc:
        logger.error(f"Failed to send SMS: {str(exc)}")
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)


# ============================================
# Celery Signals
# ============================================

from celery.signals import (
    worker_ready,
    worker_shutdown,
    task_prerun,
    task_postrun,
    task_failure,
)


@worker_ready.connect
def on_worker_ready(**kwargs):
    """Called when worker is ready"""
    logger.info("✅ Celery worker is ready")


@worker_shutdown.connect
def on_worker_shutdown(**kwargs):
    """Called when worker shuts down"""
    logger.info("🛑 Celery worker shutting down")


@task_prerun.connect
def on_task_prerun(task_id, task, *args, **kwargs):
    """Called before task execution"""
    logger.debug(f"Task {task.name} starting (ID: {task_id})")


@task_postrun.connect
def on_task_postrun(task_id, task, *args, **kwargs):
    """Called after task execution"""
    logger.debug(f"Task {task.name} completed (ID: {task_id})")


@task_failure.connect
def on_task_failure(task_id, exception, *args, **kwargs):
    """Called when task fails"""
    logger.error(f"Task failed (ID: {task_id}): {str(exception)}")


# ============================================
# Celery Health Check
# ============================================

def check_celery_health() -> bool:
    """
    Check if Celery workers are running
    
    Returns:
        True if healthy, False otherwise
    """
    try:
        # Check worker status
        inspect = celery_app.control.inspect()
        stats = inspect.stats()
        
        if not stats:
            logger.warning("No Celery workers found")
            return False
        
        logger.info(f"Celery workers active: {len(stats)}")
        return True
        
    except Exception as e:
        logger.error(f"Celery health check failed: {str(e)}")
        return False


# ============================================
# Exports
# ============================================

__all__ = [
    "celery_app",
    "send_email_task",
    "process_payment_task",
    "generate_report_task",
    "backup_database_task",
    "send_sms_task",
    "check_celery_health",
]
