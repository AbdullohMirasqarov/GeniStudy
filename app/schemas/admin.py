from pydantic import BaseModel, EmailStr
from uuid import UUID

class AdminCreate(BaseModel):
    username: str
    fullname: str
    email: EmailStr
    password: str

class AdminOut(BaseModel):
    id: UUID
    username: str
    fullname: str
    email: EmailStr

    model_config = {
        "from_attributes": True
    }