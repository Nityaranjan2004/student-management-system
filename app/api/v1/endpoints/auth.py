from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import LoginRequest, RegisterRequest, RefreshTokenRequest, Token
from app.schemas.user import UserResponse
from app.models.user import User
from app.services.auth_service import AuthService
from app.api.dependencies import get_current_active_user

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db)
):
    """Public self-registration for new users."""
    service = AuthService(db)
    return service.register_user(payload)


@router.post("/login", response_model=Token)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db)
):
    """Log in with JSON payload (username/email + password) to obtain JWT token."""
    service = AuthService(db)
    return service.authenticate_user(payload)


@router.post("/swagger-login", response_model=Token, include_in_schema=False)
def swagger_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """OAuth2 compatible endpoint for Swagger UI 'Authorize' popup button."""
    service = AuthService(db)
    login_request = LoginRequest(
        username_or_email=form_data.username,
        password=form_data.password
    )
    return service.authenticate_user(login_request)


@router.post("/refresh", response_model=Token)
def refresh_token(
    payload: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """Exchange refresh token for a fresh access token."""
    service = AuthService(db)
    return service.refresh_access_token(payload.refresh_token)


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
):
    """Get profile information of the logged-in user."""
    return current_user
