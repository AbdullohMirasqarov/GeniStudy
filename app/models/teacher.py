from sqlalchemy import Column, String, Date, Boolean, Integer
from app.database import Base
import uuid
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fullname = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    avatar = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=True)
    birthday = Column(Date, nullable=True)
    hashed_password = Column(String, nullable=True)
    balance = Column(Integer, default=0)
    is_verified = Column(Boolean, default=False)

    courses = relationship("Course", back_populates="teacher")