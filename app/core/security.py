from datetime import datetime, timedelta, timezone
from typing import Union, Any, Optional
import jwt
from passlib.context import CryptContext
from app.core.config import settings

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

# 🔒 1. PASSWORD HASHING
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its bcrypt hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password with bcrypt before saving to DB."""
    return pwd_context.hash(password)



# 🎟️ 2. JWT TOKEN CREATION & VERIFICATION
def create_access_token(
    subject: Union[str, Any],
    role: str,
    user_id: int,
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create a signed JWT access token."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "exp": expire,
        "sub": str(subject),      # username or email
        "user_id": user_id,
        "role": role,
        "type": "access"
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)



def create_refresh_token(
    subject: Union[str, Any],
    user_id: int,
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create a long-lived signed JWT refresh token."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {
        "exp": expire,
        "sub": str(subject),
        "user_id": user_id,
        "type": "refresh"
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)





def decode_token(token: str) -> Optional[dict]:
    """Decode and validate JWT token signature and expiration."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None