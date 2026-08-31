from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.db.init_db import init_db
from app.api.v1.router import api_router
import app.models  # Registers all models with Base.metadata


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager: handles startup and shutdown events."""
    # 1. Create tables in PostgreSQL on startup
    Base.metadata.create_all(bind=engine)
    
    # 2. Seed default Admin user
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()
        
    yield  # App runs while paused here


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include all v1 API routes
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    return {
        "message": "Welcome to Student Management System API",
        "docs_url": "/docs",
        "version": "1.0.0"
    }
