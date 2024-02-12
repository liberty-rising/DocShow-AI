from typing import Dict, Union

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
    table_name = Column(String)

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
            "table_name": self.table_name,
        }


class DataProfileCreateRequest(BaseModel):
    """
    DataProfileCreateRequest Model
    ------------------------------
    This class represents the request body for creating a new data profile.
    Attributes:
    - name: The name of the data profile.
    - extract_instructions: The instructions for extracting data from the file.
    - column_metadata: A dictionary where each key is a column name and each value is another dictionary specifying the attributes of the column.
        The inner dictionary includes 'data_type' and 'primary_key' fields.
    """

    name: str
    extract_instructions: str
    column_metadata: Dict[str, Dict[str, Union[str, bool]]]


class DataProfileCreateResponse(BaseModel):
    name: str
    extract_instructions: str


class SuggestedColumnTypesRequest(BaseModel):
    data: list
