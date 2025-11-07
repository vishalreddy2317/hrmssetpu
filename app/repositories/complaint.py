from app.crud.complaint import complaint_crud


class ComplaintRepository:
    def __init__(self):
        self.crud = complaint_crud


complaint_repository = ComplaintRepository()