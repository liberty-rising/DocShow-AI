from enum import Enum
from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from typing import Optional

Base = declarative_base()

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

class User(Base):
    """
    Represents a user interacting with the app.

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
    hashed_password = Column(String)
    organization = Column(String, nullable=True)
    role = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())

class UserCreate(BaseModel):
    """
    Pydantic model representing the data required to create a new user.

    Attributes:
        username (str): The desired username for the new user.
        email (EmailStr): The email address of the user.
        password (str): The password for the new user, unhashed.
        organization (Optional[str]): The organization the user belongs to, if any.
        role (Optional[str]): The role or position of the user within the organization, if specified.
    """
    username: str
    email: EmailStr
    password: str
    organization: Optional[str] = None
    role: Optional[str] = None

class UserOut(BaseModel):
    """
    UserOut is a Pydantic model representing non-sensitive user data.

    This model is designed to be used as a response model for API endpoints
    that retrieve user information. It ensures sensitive information, such
    as hashed passwords, is not exposed in API responses.

    Attributes:
        id (int): The unique identifier for each user.
        username (str): The username chosen by the user.
        email (EmailStr): The email address of the user.
        organization (Optional[str]): The organization the user belongs to. Can be None.
        role (Optional[str]): The role or designation of the user. Can be None.
    """
    id: int
    username: str
    email: EmailStr
    organization: Optional[str]
    role: Optional[str]

class UserRole(str, Enum):
    NONE = None
    GUEST = "guest"
    USER = "user"
    ADMIN = "admin"

class UserUpdate(BaseModel):
    """
    Model representing the data required to update a user's details.

    Attributes:
    - username (str): The unique username of the user. This will be used as a key to find and update the user.
    - organization (Optional[str]): The organization to which the user belongs. If not provided, the organization will not be updated.
    - role (Optional[str]): The role assigned to the user within the system or organization. If not provided, the role will not be updated.

    This model is used when making requests to update user details.
    """
    username: str
    organization: Optional[str]
    role: Optional[UserRole]