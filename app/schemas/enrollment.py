from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.common import BaseSchema, TimestampSchema
from app.schemas.student import StudentResponse
from app.schemas.course import CourseResponse


class EnrollmentStatus(str, Enum):
    ENROLLED = "enrolled"
    COMPLETED = "completed"
    DROPPED = "dropped"
    PENDING = "pending"




class EnrollmentBase(BaseModel):
    student_id: int = Field(..., description="ID of the student")
    course_id: int = Field(..., description="ID of the course")
    status: EnrollmentStatus = EnrollmentStatus.ENROLLED
    grade: Optional[str] = Field(None, max_length=10, description="Grade e.g. A, B+, 95.0")


class EnrollmentCreate(EnrollmentBase):
    """Payload to enroll a student in a course."""
    pass


class EnrollmentUpdate(BaseModel):
    """Payload to update status or assign grade."""
    status: Optional[EnrollmentStatus] = None
    grade: Optional[str] = Field(None, max_length=10)




class EnrollmentResponse(BaseSchema, TimestampSchema):
    """Standard enrollment response."""
    id: int
    student_id: int
    course_id: int
    status: EnrollmentStatus
    grade: Optional[str] = None
    enrolled_at: Optional[datetime] = None


class EnrollmentDetailResponse(EnrollmentResponse):
    """Detailed enrollment response including full student and course objects."""
    student: Optional[StudentResponse] = None
    course: Optional[CourseResponse] = None
