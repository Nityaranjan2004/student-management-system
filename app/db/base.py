from datetime import datetime
from sqlalchemy import Column,DateTime
from sqlalchemy.orm import declarative_base,declared_attr



class CustomBase:
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"


Base  =declarative_base(cls=CustomBase)


class TimestampMixin:
    """Mixin that adds created_at and updated_at timestamp columns."""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )