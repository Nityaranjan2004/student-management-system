from typing import Optional
from pydantic import BaseModel,EmailStr,Field

class LoginRequest(BaseModel):
    username_or_email:str = Field(...,description="Username or Email address")
    password: str = Field(..., min_length=6, description="Account password")




class RegisterRequest(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=6, description="Account password")



class RefreshTokenRequest(BaseModel):
    refresh_token: str


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(..., min_length=6)
    new_password: str = Field(..., min_length=6)


class PasswordResetRequest(BaseModel):
    email: EmailStr




class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(..., min_length=6)



class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: Optional[int] = None



class TokenPayload(BaseModel):
    sub: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[str] = None
    exp: Optional[int] = None