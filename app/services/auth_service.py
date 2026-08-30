from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest, Token
from app.schemas.user import UserCreate, UserRole
from app.models.user import User
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
)


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def register_user(self, register_data: RegisterRequest) -> User:
        """Register a new student/user account."""
        # 1. Check if email already registered
        if self.user_repo.get_by_email(register_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists."
            )

        # 2. Check if username is taken
        if self.user_repo.get_by_username(register_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this username already exists."
            )

        # 3. Hash password and save user
        hashed_password = get_password_hash(register_data.password)
        user_create_schema = UserCreate(
            email=register_data.email,
            username=register_data.username,
            first_name=register_data.first_name,
            last_name=register_data.last_name,
            password=register_data.password,
            role=UserRole.STUDENT,  # Default public registration is STUDENT
            is_active=True
        )
        return self.user_repo.create(user_create_schema, hashed_password)

    def authenticate_user(self, login_data: LoginRequest) -> Token:
        """Authenticate user credentials and return JWT tokens."""
        user = self.user_repo.get_by_username_or_email(login_data.username_or_email)
        
        if not user or not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username/email or password.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive. Please contact admin."
            )

        # Generate JWT Tokens
        access_token = create_access_token(
            subject=user.username,
            role=user.role.value,
            user_id=user.id
        )
        refresh_token = create_refresh_token(
            subject=user.username,
            user_id=user.id
        )

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )

    def refresh_access_token(self, refresh_token: str) -> Token:
        """Exchange valid refresh token for a new access token."""
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token."
            )

        username = payload.get("sub")
        user = self.user_repo.get_by_username(username)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive."
            )

        new_access_token = create_access_token(
            subject=user.username,
            role=user.role.value,
            user_id=user.id
        )
        return Token(
            access_token=new_access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
