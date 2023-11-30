from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func
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
    - organization: The organization associated with the data profile.

    The class also includes methods for initialization and converting the model instance into a dictionary.
    """

    __tablename__ = "dataprofile"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    file_type = Column(String)
    organization = Column(String)

    def __init__(self, id, name, file_type, organization):
        self.name = name
        self.file_type = file_type
        self.organization = organization
    
    
    def to_dict(self):
        """
        Converts the DataProfile instance into a dictionary.
        """
        return {
            "id": self.id,
            "name": self.name,
            "file_type": self.file_type,
            "organization": self.organization
        }