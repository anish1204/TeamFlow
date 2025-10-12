import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Load environment variables from .env
load_dotenv()

# Read DATABASE_URL from environment
URL_DATABASE = os.getenv("DATABASE_URL")

if not URL_DATABASE:
    raise ValueError("DATABASE_URL not found. Please set it in the .env file.")

# Initialize SQLAlchemy
engine = create_engine(URL_DATABASE, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
