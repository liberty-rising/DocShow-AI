from sqlalchemy import Column, Integer, String, ForeignKey
from pydantic import BaseModel
from .base import Base


class DataProfile(Base):
    __tablename__ = "data_profiles"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    file_type = Column(String)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    description = Column(String)  # New description column

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "file_type": self.file_type,
            "organization_id": self.organization_id,
            "description": self.description,  # Include description in the dictionary
        }


class DataProfileCreateRequest(BaseModel):
    name: str
    description: str  # Include description here


class DataProfileCreateResponse(BaseModel):
    name: str
    description: str  # Include description here
