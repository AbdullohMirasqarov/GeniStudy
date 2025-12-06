# models/purchase.py
from sqlalchemy import Column, String, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from ..database import Base

class PaymentStatus(enum.Enum):
    pending = "pending"
    paid = "paid"
    failed = "failed"

class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"))
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"))
    amount = Column(Integer)  # so'mda
    status = Column(Enum(PaymentStatus), default=PaymentStatus.pending)
    created_at = Column(DateTime, default=datetime.utcnow)
    paid_at = Column(DateTime, nullable=True)

    student = relationship("Student")
    course = relationship("Course")
