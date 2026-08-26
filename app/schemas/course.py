from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.common import BaseSchema, TimestampSchema
from app.schemas.teacher import TeacherResponse




class CourseBase(BaseModel):
    code: str = Field(..., min_length=2, max_length=20, description="e.g. CS101")
    title: str = Field(..., min_length=2, max_length=150)
    description: Optional[str] = None
    credits: int = Field(default=3, ge=1, le=10)
    department: Optional[str] = Field(None, max_length=100)
    semester: Optional[str] = Field(None, max_length=50)
    is_active: bool = True


class CourseCreate(CourseBase):
    """Payload to create a new course."""
    teacher_id: Optional[int] = Field(None, description="Assigned Teacher ID")


class CourseUpdate(BaseModel):
    """Payload to update course information."""
    code: Optional[str] = Field(None, min_length=2, max_length=20)
    title: Optional[str] = Field(None, min_length=2, max_length=150)
    description: Optional[str] = None
    credits: Optional[int] = Field(None, ge=1, le=10)
    department: Optional[str] = Field(None, max_length=100)
    semester: Optional[str] = Field(None, max_length=50)
    teacher_id: Optional[int] = None
    is_active: Optional[bool] = None




class CourseResponse(BaseSchema, TimestampSchema):
    """Standard course response."""
    id: int
    code: str
    title: str
    description: Optional[str] = None
    credits: int
    department: Optional[str] = None
    semester: Optional[str] = None
    is_active: bool
    teacher_id: Optional[int] = None


class CourseDetailResponse(CourseResponse):
    """Detailed course response with teacher details."""
    teacher: Optional[TeacherResponse] = None
