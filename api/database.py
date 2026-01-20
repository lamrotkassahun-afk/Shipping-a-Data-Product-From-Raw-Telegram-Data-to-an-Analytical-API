from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres@localhost:5434/sales"

# The engine is what actually talks to the DB
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# This creates a "Session" which is a single connection for a request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get a DB session for our API routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()