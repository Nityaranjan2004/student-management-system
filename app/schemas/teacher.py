from datetime import date
from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.common import BaseSchema, TimestampSchema
from app.schemas.user import UserResponse, UserCreate


# ==========================================
# 📥 REQUEST SCHEMAS
# ==========================================

class TeacherBase(BaseModel):
    employee_id: str = Field(..., max_length=50, description="Unique teacher employee ID")
    department: str = Field(..., max_length=100)
    qualification: Optional[str] = Field(None, max_length=100)
    specialization: Optional[str] = Field(None, max_length=150)
    phone: Optional[str] = Field(None, max_length=20)
    hire_date: Optional[date] = None


class TeacherCreate(TeacherBase):
    """Payload to create teacher + user account together."""
    user: UserCreate


class TeacherCreateWithUserId(TeacherBase):
    """Payload to create teacher profile for existing user ID."""
    user_id: int


class TeacherUpdate(BaseModel):
    """Payload to update teacher profile."""
    employee_id: Optional[str] = Field(None, max_length=50)
    department: Optional[str] = Field(None, max_length=100)
    qualification: Optional[str] = Field(None, max_length=100)
    specialization: Optional[str] = Field(None, max_length=150)
    phone: Optional[str] = Field(None, max_length=20)
    hire_date: Optional[date] = None


# ==========================================
# 📤 RESPONSE SCHEMAS
# ==========================================

class TeacherResponse(BaseSchema, TimestampSchema):
    """Standard teacher profile response."""
    id: int
    user_id: int
    employee_id: str
    department: str
    qualification: Optional[str] = None
    specialization: Optional[str] = None
    phone: Optional[str] = None
    hire_date: Optional[date] = None
    user: Optional[UserResponse] = None


class TeacherDetailResponse(TeacherResponse):
    """Detailed teacher profile response."""
    pass
