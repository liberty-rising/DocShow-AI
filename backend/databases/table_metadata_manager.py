"""
This module provides a TableMetadataManager class to manage operations related to the TableMetadata model.
It facilitates CRUD operations and formatting of table metadata information.
"""
from sqlalchemy.orm import Session
from typing import List
from models.table_metadata import TableMetadata


class TableMetadataManager:
    """
    A class to manage operations related to the TableMetadata model.
    
    Attributes:
        db_session (Session): An active database session for performing operations.
    """
    def __init__(self, db_session: Session):
        """
        Initializes the TableMetadataManager with the given database session.
        
        Args:
            db_session (Session): The database session to be used for operations.
        """
        self.db_session = db_session

    def get_all_metadata(self) -> List[TableMetadata]:
        """
        Retrieve all table metadata from the database.
        
        Returns:
            List[TableMetadata]: List of TableMetadata objects.
        """
        try:
            return self.db_session.query(TableMetadata).all()
        except Exception as e:
            # Handle exception
            print(f"Database error: {str(e)}")
    
    def get_metadata(self, table_name: str) -> TableMetadata:
        """Retrieve metadata for a single table"""
        try:
            return self.db_session.query(TableMetadata).filter(
                TableMetadata.table_name == table_name
            ).first()
        except Exception as e:
            print(f"Database error: {str(e)}")
    
    def format_table_metadata_for_llm(self, rows: List[TableMetadata]) -> str:
        """
        Format a list of TableMetadata objects into a human-readable string.
        
        Args:
            rows (List[TableMetadata]): List of TableMetadata objects.
            
        Returns:
            str: Formatted metadata string.
        """
        formatted_metadata = '\n'.join(
            f"Table: {row.table_name}\nCreate Statement: {row.create_statement}\nDescription: {row.description}"
            for row in rows
        )
        return formatted_metadata

    def add_table_metadata(self, table_name: str, create_query: str, description: str):
        """
        Store table metadata in the database.
        
        Args:
            table_name (str): Name of the table.
            create_query (str): SQL create statement of the table.
            description (str): Description of the table.
        """
        try:
            table_metadata = TableMetadata(
                table_name=table_name, 
                create_statement=create_query, 
                description=description
            )
            self.db_session.merge(table_metadata)
            self.db_session.commit()
        except Exception as e:
            # Handle exception
            print(f"Database error: {str(e)}")