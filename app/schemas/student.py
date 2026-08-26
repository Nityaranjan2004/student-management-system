from datetime import date
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.common import BaseSchema, TimestampSchema
from app.schemas.user import UserResponse, UserCreate


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"



class StudentBase(BaseModel):
    roll_number: str = Field(..., max_length=50, description="Unique student roll number")
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    grade_level: Optional[str] = Field(None, max_length=50)
    section: Optional[str] = Field(None, max_length=20)
    guardian_name: Optional[str] = Field(None, max_length=100)
    guardian_phone: Optional[str] = Field(None, max_length=20)
    guardian_email: Optional[str] = None
    address: Optional[str] = None


class StudentCreate(StudentBase):
    """Payload to create student + new user account together."""
    user: UserCreate


class StudentCreateWithUserId(StudentBase):
    """Payload to create student profile for existing user ID."""
    user_id: int


class StudentUpdate(BaseModel):
    """Payload to update student profile."""
    roll_number: Optional[str] = Field(None, max_length=50)
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    grade_level: Optional[str] = Field(None, max_length=50)
    section: Optional[str] = Field(None, max_length=20)
    guardian_name: Optional[str] = Field(None, max_length=100)
    guardian_phone: Optional[str] = Field(None, max_length=20)
    guardian_email: Optional[str] = None
    address: Optional[str] = None




class StudentResponse(BaseSchema, TimestampSchema):
    """Standard student profile response."""
    id: int
    user_id: int
    roll_number: str
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    grade_level: Optional[str] = None
    section: Optional[str] = None
    guardian_name: Optional[str] = None
    guardian_phone: Optional[str] = None
    guardian_email: Optional[str] = None
    address: Optional[str] = None
    user: Optional[UserResponse] = None


class StudentDetailResponse(StudentResponse):
    """Detailed student response including account details."""
    pass
