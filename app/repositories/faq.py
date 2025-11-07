from app.crud.faq import faq_crud


class FAQRepository:
    def __init__(self):
        self.crud = faq_crud


faq_repository = FAQRepository()