from app.crud.base import CRUDBase
from app.models.notification import Notification
from app.schemas.notification import NotificationCreate, NotificationUpdate

notification_crud = CRUDBase[Notification, NotificationCreate, NotificationUpdate](Notification)