from sqlalchemy import Column, String
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from ..database import Base

class Admin(Base):
    __tablename__ = "admins"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String, unique=True, nullable=False)
    fullname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
