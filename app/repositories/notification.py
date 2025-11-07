from app.crud.notification import notification_crud


class NotificationRepository:
    def __init__(self):
        self.crud = notification_crud


notification_repository = NotificationRepository()