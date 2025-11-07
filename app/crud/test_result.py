from app.crud.base import CRUDBase
from app.models.test_result import TestResult
from app.schemas.test_result import TestResultCreate, TestResultUpdate

test_result_crud = CRUDBase[TestResult, TestResultCreate, TestResultUpdate](TestResult)