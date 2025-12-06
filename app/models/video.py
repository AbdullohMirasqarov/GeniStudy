from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import LargeBinary
from typing import Optional

class Video(Base):
    __tablename__ = "videos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    order = Column(Integer)
    video_url = Column(String, nullable=True)  # <-- Shunaqa bo'lishi kerak
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"))

    course = relationship("Course", back_populates="videos")