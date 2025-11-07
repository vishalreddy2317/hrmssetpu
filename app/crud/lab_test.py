from app.crud.base import CRUDBase
from app.models.lab_test import LabTest
from app.schemas.lab_test import LabTestCreate, LabTestUpdate

lab_test_crud = CRUDBase[LabTest, LabTestCreate, LabTestUpdate](LabTest)