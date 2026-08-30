from fastapi import APIRouter
from app.api.v1.endpoints import auth

api_router = APIRouter()

# Include auth routes under /api/v1/auth
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
