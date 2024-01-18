import re
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator
from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from .base import Base


class UserRole(str, Enum):
    NONE = "none"
    GUEST = "guest"
    ORG_MEMBER = "org_member"
    ORG_ADMIN = "org_admin"
    SYSTEM_ADMIN = "system_admin"


class User(Base):
    """
    Represents a user interacting with the app.

    Attributes:
        id (int): The unique identifier for each user.
        username (str): The username chosen by the user.
        email (str): The email address of the user.
        hashed_password (str): The hashed password for the user.
        organization_id (int): Foreign key linking the user to their organization.
        role (str, optional): The role of the user within the organization.
        subscribe_to_updates (bool): Indicates whether the user wants to receive updates.
        receive_marketing_content (bool): Indicates whether the user wants to receive marketing content.
        requires_password_update (bool): Indicates whether the user needs to update their password.
        verification_token (str, optional): The email verification token for the user.
        email_verified (bool): Indicates whether the user's email has been verified.
        created_at (datetime): The timestamp when the user was created.
        refresh_token (str, optional): The refresh token for the user.
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    role = Column(SQLEnum(UserRole), nullable=True)
    subscribe_to_updates = Column(Boolean, default=True)
    receive_marketing_content = Column(Boolean, default=True)
    requires_password_update = Column(Boolean, default=False)
    verification_token = Column(String, unique=True, index=True)
    email_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    refresh_token = Column(Text, nullable=True)


class UserCreate(BaseModel):
    """
    Pydantic model representing the data required to create a new user.

    Attributes:
        username (str): The desired username for the new user.
        email (EmailStr): The email address of the user.
        password (str): The password for the new user, unhashed.
        organization_id (Optional[int]): The id of the organization the user belongs to, if any.
        role (Optional[str]): The role or position of the user within the organization, if specified.
        subscribe_to_updates (Optional[bool]): Whether the user wants to subscribe to updates. Defaults to True.
        receive_marketing_content (Optional[bool]): Whether the user wants to receive marketing content. Defaults to True.
        requires_password_update (Optional[bool]): Whether the user is required to update their password. Defaults to False.
    """

    username: str
    email: EmailStr
    password: str
    organization_id: Optional[int] = None
    role: Optional[str] = None
    subscribe_to_updates: Optional[bool] = True
    receive_marketing_content: Optional[bool] = True
    requires_password_update: Optional[bool] = False

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password should have at least 8 characters")
        if not re.search(r"\d", v):
            raise ValueError("Password should contain at least one digit")
        if not re.search(r"\W", v):
            raise ValueError("Password should contain at least one symbol")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password should contain at least one uppercase letter")
        return v


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
        organization_id (Optional[int]): The id of the organization the user belongs to. Can be None.
        role (Optional[str]): The role or designation of the user. Can be None.
    """

    id: int
    username: str
    email: EmailStr
    organization_id: Optional[int]
    role: Optional[str]
    requires_password_update: bool
    email_verified: bool


class UserUpdate(BaseModel):
    """
    Model representing the data required to update a user's details.

    Attributes:
    - username (str): The unique username of the user. This will be used as a key to find and update the user.
    - organization_id (Optional[int]): The id of the organization to which the user belongs. If not provided, the organization id will not be updated.
    - role (Optional[str]): The role assigned to the user within the system or organization. If not provided, the role will not be updated.

    This model is used when making requests to update user details.
    """

    username: str
    organization_id: Optional[int]
    role: Optional[UserRole]
    requires_password_update: Optional[bool] = False


class ChangePasswordRequest(BaseModel):
    old_password: str = Field(...)
    new_password: str = Field(...)

    @validator("new_password")
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password should have at least 8 characters")
        if not re.search(r"\d", v):
            raise ValueError("Password should contain at least one digit")
        if not re.search(r"\W", v):
            raise ValueError("Password should contain at least one symbol")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password should contain at least one uppercase letter")
        return v


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class DeleteUserRequest(BaseModel):
    username: str


class ResetPasswordRequest(BaseModel):
    token: str = Field(...)
    new_password: str = Field(...)
    confirm_password: str = Field(...)

    @validator("new_password")
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password should have at least 8 characters")
        if not re.search(r"\d", v):
            raise ValueError("Password should contain at least one digit")
        if not re.search(r"\W", v):
            raise ValueError("Password should contain at least one symbol")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password should contain at least one uppercase letter")
        return v


class SendVerificationEmailRequest(BaseModel):
    email: str = Field(...)


class VerifyEmailRequest(BaseModel):
    token: str = Field(...)
