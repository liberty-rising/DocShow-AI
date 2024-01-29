from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint

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
    - extract_instructions: The instructions for extracting data from the file.
    The class also is converting the model instance into a dictionary.
    """

    __tablename__ = "data_profiles"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    file_type = Column(String)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    extract_instructions = Column(String)
    table_id = Column(Integer)

    __table_args__ = (
        UniqueConstraint("name", "organization_id", name="uq_name_organization_id"),
    )

    def to_dict(self):
        """
        Converts the DataProfile instance into a dictionary.
        """
        return {
            "id": self.id,
            "name": self.name,
            "file_type": self.file_type,
            "organization_id": self.organization_id,
            "extract_instructions": self.extract_instructions,
            "table_id": self.table_id,
        }


class DataProfileCreateRequest(BaseModel):
    name: str
    extract_instructions: str
    column_names_and_types: dict


class DataProfileCreateResponse(BaseModel):
    name: str
    extract_instructions: str


class SuggestedColumnTypesRequest(BaseModel):
    data: list
