from sqlalchemy import Column, Integer, String

from .base import Base


class TableMap(Base):
    """
    Represents a mapping between an organization and a table.

    Attributes:
        id (int): The unique identifier of the mapping.
        organization_id (int): The ID of the organization.
        table_name (str): The name of the table.
        table_alias (str): The alias for the table.
    """

    __tablename__ = "table_map"

    id = Column(Integer, primary_key=True, autoincrement=True)
    organization_id = Column(Integer)
    table_name = Column(String, unique=True)
    table_alias = Column(String)
