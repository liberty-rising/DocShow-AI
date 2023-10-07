from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL Configuration
# The SQLite database is located in the same directory as where the FastAPI application runs.
# In a Dockerized environment, the working directory is set to '/app/backend'.
# Therefore, './client_database.db' refers to the database file located at '/app/backend/client_database.db'.
DATABASE_URL = "sqlite:///./client_database.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base: DeclarativeMeta = declarative_base()
