from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from typing import List, Optional
from models.client_models import TableMetadata

import pandas as pd


class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.engine = create_engine(f'postgresql://admin:admin@postgres_db:5432/{db_name}')

    def __enter__(self):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()

class AppDatabaseManager(DatabaseManager):
    def __init__(self):
        super().__init__('app_db')

class ClientDatabaseManager(DatabaseManager):
    def __init__(self):
        super().__init__('client_db')

class SQLExecutor:
    def __init__(self, session: Session):
        self.session = session
        self.database_type = "postgres"
    
    def append_df_to_table(self, df: pd.DataFrame, table_name: str):
        try:
            df.to_sql(table_name, self.session.bind, if_exists='append', index=False)
        except Exception as e:
            print(f"An error occurred while appending data to table {table_name}: {str(e)}")
            raise
            
    def execute_create_query(self, query: str):
        try:
            self.session.execute(text(query))
            self.session.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            self.session.rollback()
            raise
    
    def generate_query_for_all_table_names(self):
        if self.database_type == "sqlite":
            return "SELECT name FROM sqlite_master WHERE type='table';"
        elif self.database_type == "postgres":
            return "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
        else:
            return ""
    
    def get_all_table_names(self) -> str:
        try:
            query = self.generate_query_for_all_table_names()
            result = self.session.execute(text(query))
            table_names = [row[0] for row in result]
            table_names_str = ', '.join(table_names)
            return table_names_str
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

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