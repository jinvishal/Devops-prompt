from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# We will use the same SQLite database file created by Alembic.
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    # The `connect_args` are needed only for SQLite.
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a DB session for each request.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
