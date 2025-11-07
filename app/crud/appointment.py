from app.crud.base import CRUDBase
from app.models.appointment import Appointment
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate

appointment_crud = CRUDBase[Appointment, AppointmentCreate, AppointmentUpdate](Appointment)