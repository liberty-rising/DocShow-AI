from sqlalchemy import Column, Integer, String, ForeignKey
from pydantic import BaseModel
from .base import Base


class DataProfile(Base):

    """
    DataProfile Model
    -----------------
    This class represents the 'dataprofile' table in the database.
    Attributes:
    - id: A unique identifier for each data profile.
    - name: The name of the data profile.
    - file_type: The type of file associated with the data profile.
    - organization_id: The organization associated with the data profile.
    - description: The description of the data profile.
    The class also is converting the model instance into a dictionary.
    """

    __tablename__ = "data_profiles"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    file_type = Column(String)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    description = Column(String)  # New description column

    def to_dict(self):
        """
        Converts the DataProfile instance into a dictionary.
        """
        return {
            "id": self.id,
            "name": self.name,
            "file_type": self.file_type,
            "organization_id": self.organization_id,
            "description": self.description,
        }


class DataProfileCreateRequest(BaseModel):
    name: str
    description: str


class DataProfileCreateResponse(BaseModel):
    name: str
    description: str
