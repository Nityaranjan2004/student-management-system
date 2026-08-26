from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin


class Course(Base, TimestampMixin):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(20), unique=True, index=True, nullable=False)  # e.g. "CS101"
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    credits = Column(Integer, default=3, nullable=False)
    department = Column(String(100), nullable=True)
    semester = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="SET NULL"), nullable=True)

    # Relationships
    teacher = relationship("Teacher", back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Course id={self.id} code='{self.code}' title='{self.title}'>"
