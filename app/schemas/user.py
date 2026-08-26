from pydantic._internal._validators import min_length_validator
from enum import Enum
from typing import Optional
from pydantic  import BaseModel,EmailStr,Field
from app.schemas.common import BaseSchema,TimestampSchema



class UserRole(str, Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"


class UserBase(BaseModel):
    email:EmailStr
    userneme:str=Field(...,min_length=3,max_length=50)
    first_name:str=Field(...,min_length=1,max_length=50)
    last_name:str=Field(...,min_length=1,max_length=50)
    role:UserRole = UserRole.STUDENT
    is_active:bool=True


class userCreate(UserBase):
    password:str=Field(...,min_length=6,description="plaintext passwors")



class UserUpdate(BaseModel):
    """Payload to update an existing user."""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=6)



class UserResponse(BaseSchema, TimestampSchema):
    """Public user response (hides password)."""
    id: int
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    role: UserRole
    is_active: bool
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

        
class UserInDB(UserResponse):
    """Internal user schema with hashed password for services."""
    hashed_password: str

