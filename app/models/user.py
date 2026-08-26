from sqlalchemy import false
from sqlalchemy import null
from cryptography.utils import InterfaceNotImplemented
import enum
from sqlalchemy import Column,Integer,String,Boolean,Enum
from sqlalchemy.orm import relationship
from app.db.base import Base,TimestampMixin


class UserRole(str,enum.Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"


class user(Base,TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    email = Column(String(255),unique=True,index=True,nullable=False)
    username = Column(String(255),unique=True,index=True,nullable=False)
    hashed_password = Column(String(100),nullable=False)
    first_name = Column(String(100),nullable=false)
    last_name = Column(String(100),nullable=False)
    role = Column(Enum(UserRole),default=UserRole.STUDENT,nullable=False)
    is_active = Column(Boolean,default=True,nullable=False)
    
    student_profile = relationship("Student", back_populates="user", uselist=False, cascade="all, delete-orphan")
    teacher_profile = relationship("Teacher", back_populates="user", uselist=False, cascade="all, delete-orphan")


    def __repr__(self):
        return f"<User id={self.id} username='{self.username}' role='{self.role}'>"



        # nkynkyn