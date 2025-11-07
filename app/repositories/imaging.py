from app.crud.imaging import imaging_crud


class ImagingRepository:
    def __init__(self):
        self.crud = imaging_crud


imaging_repository = ImagingRepository()