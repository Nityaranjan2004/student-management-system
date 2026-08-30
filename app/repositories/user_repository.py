from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Fetch user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """Fetch user by email."""
        return self.db.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """Fetch user by username."""
        return self.db.query(User).filter(User.username == username).first()

    def get_by_username_or_email(self, identifier: str) -> Optional[User]:
        """Fetch user by either username or email for login."""
        return self.db.query(User).filter(
            (User.username == identifier) | (User.email == identifier)
        ).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Fetch all users with pagination."""
        return self.db.query(User).offset(skip).limit(limit).all()

    def create(self, user_data: UserCreate, hashed_password: str) -> User:
        """Insert a new user into the database."""
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            role=user_data.role,
            is_active=user_data.is_active
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, db_user: User, update_data: UserUpdate, hashed_password: Optional[str] = None) -> User:
        """Update an existing user record."""
        update_dict = update_data.model_dump(exclude_unset=True, exclude={"password"})
        
        for key, value in update_dict.items():
            setattr(db_user, key, value)
            
        if hashed_password:
            db_user.hashed_password = hashed_password
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete(self, db_user: User) -> bool:
        """Delete a user record."""
        self.db.delete(db_user)
        self.db.commit()
        return True