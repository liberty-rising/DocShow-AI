from fastapi import HTTPException, UploadFile
from typing import List

from backend.databases.client_db_config import SessionLocal
from backend.models.client_models import TableMetadata

import sqlite3
import csv


class AppDatabaseManager:
    def __init__(self):
        self.db_path = "app_database.db"
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        return self.conn
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

class ClientDatabaseManager:
    def __init__(self):
        self.db_path = "client_database.db"
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        return self.conn
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

class SQLExecutor:
    def __init__(self, conn):
        self.conn = conn
    
    def execute_create_query(self, query: str):
        with self.conn:
            cursor = self.conn.cursor()

            try:
                cursor.execute(query)
                self.conn.commit()
            except Exception as e:
                print(f"An error occurred: {e}")
    
    def append_csv_to_table(self, processed_file: UploadFile, table_name: str):
        with self.conn:
            try:
                cursor = self.conn.cursor()

                # Read the file content into a list of lists
                file_content = csv.reader(processed_file.file.read().decode().splitlines())

                # Skip the header row and prepare the data
                next(file_content)
                data_to_insert = [tuple(row) for row in file_content]

                # Prepare the SQL statement to append the data
                placeholders = ", ".join("?" * len(data_to_insert[0]))
                sql = f"INSERT INTO {table_name} VALUES ({placeholders})"

                # Execute the SQL statement
                cursor.executemany(sql, data_to_insert)
                self.conn.commit()

            except Exception as e:
                print(f"An error occurred while appending data to table {table_name}: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

class TableMetadataManager:
    def __init__(self):
        self.db_session = SessionLocal()

    def get_metadata(self) -> List[TableMetadata]:
        try:
            return self.db_session.query(TableMetadata).all()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def format_table_metadata_for_llm(rows: List[TableMetadata]) -> str:
        """
        Formats the table metadata into a natural language string suitable for querying a Large Language Model.
        
        Parameters:
        - rows (List[TableMetadata]): A list of TableMetadata objects representing the rows in the table_metadata database table.

        Returns:
        - str: A formatted string containing the table metadata.
        """
        formatted_metadata = '\n'.join(
            f"Table: {row.table_name}\nCreate Statement: {row.create_statement}\nDescription: {row.description}"
            for row in rows
        )

        return formatted_metadata

    def store_desc(self, table_name: str, create_query: str, description: str):
        # Implementation