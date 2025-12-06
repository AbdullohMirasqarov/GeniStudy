from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional
from uuid import UUID


class TeacherRegister(BaseModel):
    fullname: str
    username: str
    email: EmailStr
    # phone_number: str
    password: str

class TeacherVerify(BaseModel):
    email: EmailStr
    code: str
    # birthday: date


class TeacherLogin(BaseModel):
    username: str
    # phone_number: str
    password: str

class TeacherOut(BaseModel):
    id: UUID
    fullname: str
    username: str
    email: str
    phone_number: str
    bio: Optional[str]
    avatar: Optional[str]

    model_config = {
        "from_attributes": True
    }