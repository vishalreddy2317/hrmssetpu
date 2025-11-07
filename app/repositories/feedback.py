from app.crud.feedback import feedback_crud


class FeedbackRepository:
    def __init__(self):
        self.crud = feedback_crud


feedback_repository = FeedbackRepository()