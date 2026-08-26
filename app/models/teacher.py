from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin


class Teacher(Base, TimestampMixin):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    employee_id = Column(String(50), unique=True, index=True, nullable=False)
    department = Column(String(100), nullable=False)  # e.g. "Computer Science"
    qualification = Column(String(100), nullable=True)  # e.g. "Ph.D", "M.Tech"
    specialization = Column(String(150), nullable=True)
    phone = Column(String(20), nullable=True)
    hire_date = Column(Date, nullable=True)

    # Relationships
    user = relationship("User", back_populates="teacher_profile")
    courses = relationship("Course", back_populates="teacher")

    def __repr__(self):
        return f"<Teacher id={self.id} employee_id='{self.employee_id}' department='{self.department}'>"
