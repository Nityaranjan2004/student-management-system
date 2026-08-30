from typing import List
from pydantic_settings import BaseSettings,SettingsConfigDict

# BaseSettings: A Pydantic class that automatically 
# reads values from your .env file or operating system environment variables.

# SettingsConfigDict: Tells Pydantic how and where to read the configuration file.

class Settings(BaseSettings):
    #App information
    PROJECT_NAME:str="Student Management System"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"

    # PostgreSQL Database URL
    DATABASE_URL: str = "postgresql+psycopg://postgres:Nitya%402004@localhost:5432/StudentManagementApp"



    # JWT Authentication
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a95  fbffbb gbgfn63b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    # Load variables from .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
settings = Settings()

