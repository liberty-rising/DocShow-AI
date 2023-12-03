from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from .base import Base


class Organization(Base):
    """
    Represents an organization that holds users.
    """

    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), default=func.now())


class OrganizationCreateRequest(BaseModel):
    name: str


class OrganizationCreateResponse(BaseModel):
    name: str
