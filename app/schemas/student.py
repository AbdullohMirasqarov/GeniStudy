from pydantic import BaseModel, EmailStr
from uuid import UUID

class StudentCreate(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    password: str
    # phone_number: str

class CodeVerify(BaseModel):
    email: EmailStr
    code: str


class StudentLogin(BaseModel):
    username: str
    password: str


class StudentOut(BaseModel):
    id: UUID
    full_name: str
    username: str
    email: str
    # phone_number: str

    model_config = {
        "from_attributes": True
    } 