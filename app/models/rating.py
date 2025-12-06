from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # ForeignKey ustunlari kerak
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)

    rating_value = Column(Integer, nullable=False)

    # Relationshiplar
    course = relationship("Course", back_populates="rating")
    student = relationship("Student", back_populates="ratings")