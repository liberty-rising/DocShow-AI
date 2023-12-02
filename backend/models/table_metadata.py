from sqlalchemy import Column, String

from .base import Base


class TableMetadata(Base):
    """
    Represents metadata for a table in the database.

    Attributes:
        table_name (str): The name of the table, used as the primary key.
        create_statement (str): The SQL statement used to create the table.
        description (str): A description of the table.
    """

    __tablename__ = "table_metadata"
    table_name = Column(String, primary_key=True, index=True)
    create_statement = Column(String)
    description = Column(String)

    def to_dict(self):
        return {
            "table_name": self.table_name,
            "create_statement": self.create_statement,
            "description": self.description,
        }
