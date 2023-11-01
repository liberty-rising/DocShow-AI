from sqlalchemy.orm import Session
from typing import List
from models.client_models import TableMetadata


class TableMetadataManager:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_metadata(self) -> List[TableMetadata]:
        try:
            return self.db_session.query(TableMetadata).all()
        except Exception as e:
            # Handle exception
            print(f"Database error: {str(e)}")
    
    def format_table_metadata_for_llm(self, rows: List[TableMetadata]) -> str:
        formatted_metadata = '\n'.join(
            f"Table: {row.table_name}\nCreate Statement: {row.create_statement}\nDescription: {row.description}"
            for row in rows
        )
        return formatted_metadata

    def store_table_desc(self, table_name: str, create_query: str, description: str):
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