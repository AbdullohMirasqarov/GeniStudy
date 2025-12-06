from sqlalchemy import Column, String, BigInteger, ForeignKey, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import LargeBinary
from app.models.video import Video


class CourseCategory(Base):
    __tablename__ = "course_categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, default="")
    subcategories = relationship("CourseSubCategory", back_populates="category", cascade="all, delete")


class CourseSubCategory(Base):
    __tablename__ = "course_subcategories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("course_categories.id"))
    category = relationship("CourseCategory", back_populates="subcategories")

    courses = relationship("Course", back_populates="subcategory")



class Course(Base):
    __tablename__ = "courses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)

    category_id = Column(UUID(as_uuid=True), ForeignKey("course_categories.id"), nullable=False)
    subcategory_id = Column(UUID(as_uuid=True), ForeignKey("course_subcategories.id"), nullable=True)

    category = relationship("CourseCategory")
    subcategory = relationship("CourseSubCategory", back_populates="courses")

    teacher_id = Column(UUID(as_uuid=True), ForeignKey("teachers.id"))
    teacher = relationship("Teacher", back_populates="courses")

    videos = relationship("Video", back_populates="course", cascade="all, delete")
    rating = relationship("Rating", back_populates="course", cascade="all, delete")
    image_url = Column(String)
