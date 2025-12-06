from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from ..database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Student(Base):
    __tablename__ = "students"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, nullable=True)
    hashed_password = Column(String)
    ratings = relationship("Rating", back_populates="student", cascade="all, delete")