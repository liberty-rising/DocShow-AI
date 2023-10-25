from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    """
    Represents a user interacting with the LLM.

    Attributes:
        id (int): The unique identifier for each user.
        username (str): The username chosen by the user.
        email (str): The email address of the user.
        created_at (datetime): The timestamp when the user was created.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    created_at = Column(DateTime(timezone=True), default=func.now())