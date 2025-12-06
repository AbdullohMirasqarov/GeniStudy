from pydantic import BaseModel
from uuid import UUID

class RatingCreate(BaseModel):
    course_id: UUID
    student_id: UUID
    rating_value: int

class RatingOut(BaseModel):
    id: UUID
    course_id: UUID
    student_id: UUID
    rating_value: int

    model_config = {
        "from_attributes": True
    }