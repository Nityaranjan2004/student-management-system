from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
from app.core.config import settings


# Optimized for PostgreSQL with connection pooling it is the connection pipeline
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=False
)

# pool_pre_ping=True: Before executing any query, SQLAlchemy sends a quick "ping" 
# to check if the PostgreSQL connection is still alive. If PostgreSQL restarted or 
# dropped the connection, it automatically reconnects

# pool_size=10: Keeps 10 open database connections in memory ready for incoming requests 
# (saves the time of opening a new socket connection for each request).


# max_overflow=20: Under heavy traffic, allows up to 20 extra temporary connections 
# (total: 30 connections).

# echo=False: If set to True, it prints every generated raw SQL query in your terminal 
# (useful for debugging).




# The Session Factory
SessionLocal = sessionmaker(
    autocommit = False,
    autoflush=False,
    bind=engine
)


# db = SessionLocal(): Opens a fresh database session for an incoming HTTP request.
# yield db: Pauses the function and hands the session over to your endpoint 
# function so it can query data.
# finally: db.close(): When the HTTP request finishes (or even if an error occurs), the 
# finally block guarantees the database session is closed and returned to the connection pool, 
# preventing connection leaks.



def get_db() -> Generator[Session,None,None]:
    """
    FastAPI dependency yielding a database session per request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
