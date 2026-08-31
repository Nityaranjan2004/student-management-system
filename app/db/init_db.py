from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import UserRole
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


def init_db(db: Session) -> None:
    """Seed the database with the default Super Admin user if not present."""
    user_repo = UserRepository(db)
    
    # Check if admin already exists
    admin_user = user_repo.get_by_email(settings.FIRST_SUPERUSER_EMAIL) or user_repo.get_by_username(settings.FIRST_SUPERUSER_USERNAME)
    
    if not admin_user:
        hashed_password = get_password_hash(settings.FIRST_SUPERUSER_PASSWORD)
        admin_data = UserCreate(
            email=settings.FIRST_SUPERUSER_EMAIL,
            username=settings.FIRST_SUPERUSER_USERNAME,
            first_name="System",
            last_name="Administrator",
            password=settings.FIRST_SUPERUSER_PASSWORD,
            role=UserRole.ADMIN,
            is_active=True
        )
        user_repo.create(admin_data, hashed_password)
        print(f"🚀 [SEED] Default Admin created successfully!")
        print(f"   📧 Email:    {settings.FIRST_SUPERUSER_EMAIL}")
        print(f"   👤 Username: {settings.FIRST_SUPERUSER_USERNAME}")
        print(f"   🔑 Password: {settings.FIRST_SUPERUSER_PASSWORD}")
    else:
        print(f"ℹ️ [SEED] Admin user already exists: {admin_user.username}")
