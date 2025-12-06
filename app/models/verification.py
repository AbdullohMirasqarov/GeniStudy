import uuid
from sqlalchemy import Column, Integer, String, DateTime
from ..database import Base
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID

class VerificationCodeTeacher(Base):
    __tablename__ = "verification_codes_teacher"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, index=True, unique=True)
    full_name = Column(String)
    username = Column(String)
    phone_number = Column(String)
    hashed_password = Column(String)
    code = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class VerificationCodeStudent(Base):
    __tablename__ = "verification_codes_student"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, index=True, unique=True)
    full_name = Column(String)
    username = Column(String)
    phone_number = Column(String, nullable=True)
    hashed_password = Column(String)
    code = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
