from typing import List

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import decode_token
from app.repositories.user_repository import UserRepository
from app.models.user import User, UserRole


# Extracts Bearer token from:
# Authorization: Bearer <JWT_TOKEN>
http_bearer = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    db: Session = Depends(get_db)
) -> User:
    """Extract and validate current logged in user from JWT Bearer token."""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Extract JWT token
    token = credentials.credentials

    # Decode and validate JWT
    payload = decode_token(token)

    if payload is None or payload.get("type") != "access":
        raise credentials_exception

    # Get username from JWT 'sub' claim
    username: str = payload.get("sub")

    if username is None:
        raise credentials_exception

    # Find user in database
    user_repo = UserRepository(db)
    user = user_repo.get_by_username(username)

    if user is None:
        raise credentials_exception

    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Ensure authenticated user is active."""

    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account."
        )

    return current_user


class RoleChecker:
    """RBAC Guard: Ensures user has one of the allowed roles."""

    def __init__(self, allowed_roles: List[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(
        self,
        current_user: User = Depends(get_current_active_user)
    ) -> User:

        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"Access denied. Required role: "
                    f"{[r.value for r in self.allowed_roles]}"
                )
            )

        return current_user


# Handy shortcut guards
require_admin = RoleChecker([UserRole.ADMIN])

require_teacher = RoleChecker([
    UserRole.ADMIN,
    UserRole.TEACHER
])

require_student = RoleChecker([
    UserRole.ADMIN,
    UserRole.STUDENT
])