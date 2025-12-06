from pydantic import BaseModel
from uuid import UUID

class TestPaymentIn(BaseModel):
    student_id: UUID
    course_id: UUID