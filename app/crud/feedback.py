from app.crud.base import CRUDBase
from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate, FeedbackUpdate

feedback_crud = CRUDBase[Feedback, FeedbackCreate, FeedbackUpdate](Feedback)