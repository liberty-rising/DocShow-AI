from fastapi import HTTPException, UploadFile
from typing import List, Optional

from backend.databases.app_db_config import SessionLocal as AppSessionLocal
from backend.databases.client_db_config import SessionLocal as ClientSessionLocal
from backend.models.client_models import TableMetadata

import csv
import re
import sqlite3


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
        self.database_type = "sqlite"
    
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
            
    def execute_create_query(self, query: str):
        with self.conn:
            cursor = self.conn.cursor()

            try:
                cursor.execute(query)
                self.conn.commit()
            except Exception as e:
                print(f"An error occurred: {e}")
    
    def generate_query_for_all_table_names(self):
        """
        Generate the SQL query required to fetch all table names in the database.
        The query is generated based on the type of database (e.g., SQLite, PostgreSQL).

        Returns:
            str: SQL query string to fetch all table names from the database.

        Note:
            TODO: Currently, only SQLite is supported. For other database types, an empty string is returned.
        """
        if self.database_type == "sqlite":
            return "SELECT name FROM sqlite_master WHERE type='table';"
        elif self.database_type == "postgres":
            return ""
        else:
            return ""
    
    def get_all_table_names(self) -> str:
        """
        Retrieves the names of all tables in the database and returns them as a comma-separated string.

        Returns:
            str: A string containing the names of all tables in the database, separated by commas.
        """
        with self.conn:
            cursor = self.conn.cursor()

            query = self.generate_query_for_all_table_names()
            cursor.execute(query)

            tables = cursor.fetchall()
            table_names = [table[0] for table in tables]

            table_names_str = ', '.join(table_names)
            
            return table_names_str

class TableMetadataManager:
    """
    Manages interactions with table metadata in a specified database.
    
    Attributes:
        db_session: SQLAlchemy database session for executing queries.
        
    Methods:
        __enter__: Context manager enter function.
        __exit__: Context manager exit function, closes the database session.
        get_metadata: Retrieves all table metadata from the database.
        format_table_metadata_for_llm: Formats table metadata for use with a Large Language Model.
        store_desc: Stores the description of a table in the database.
    """

    def __init__(self, database: str):
        """
        Initializes a new TableMetadataManager instance.
        
        Parameters:
            database (str): The type of database ("app" or "client").
        """
        if database == "app":
            self.db_session = AppSessionLocal()
        elif database == "client":
            self.db_session = ClientSessionLocal()
        else:
            raise ValueError("Invalid database specified")
    
    def __enter__(self) -> 'TableMetadataManager':
        """Context manager enter function. Returns the manager instance."""
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Context manager exit function. Closes the database session."""
        self.db_session.close()

    def get_metadata(self) -> List[TableMetadata]:
        """
        Retrieves all table metadata from the database.
        
        Returns:
            List[TableMetadata]: A list of TableMetadata objects.
            
        Raises:
            HTTPException: An exception with a 500 status code if a database error occurs.
        """
        try:
            return self.db_session.query(TableMetadata).all()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def format_table_metadata_for_llm(self, rows: List[TableMetadata]) -> str:
        """
        Formats the table metadata into a natural language string suitable for querying a Large Language Model.
        
        Parameters:
            rows (List[TableMetadata]): A list of TableMetadata objects representing the rows in the table_metadata database table.

        Returns:
            str: A formatted string containing the table metadata.
        """
        formatted_metadata = '\n'.join(
            f"Table: {row.table_name}\nCreate Statement: {row.create_statement}\nDescription: {row.description}"
            for row in rows
        )

        return formatted_metadata

    def store_table_desc(self, table_name: str, create_query: str, description: str):
        """
        Stores the description of a table in the database.
        
        Parameters:
            table_name (str): The name of the table.
            create_query (str): The SQL CREATE TABLE query for the table.
            description (str): The description of the table.
        """
        try:
            # Your database operations here
            table_metadata = TableMetadata(table_name=table_name, create_statement=create_query, description=description)
            self.db_session.merge(table_metadata)
            self.db_session.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

class SQLStringManipulator:
    def __init__(self, sql_string: str = ""):
        self.sql_string = sql_string
    
    def set_sql_string(self, sql_string: str):
        self.sql_string = sql_string
    
    def get_table_from_create_query(self) -> Optional[str]:
        """
        Extract the table name from a SQL CREATE TABLE query.
        
        Returns:
            str or None: The table name if the query is valid, otherwise None.
        """
        # Use regular expression to extract table name
        match = re.search(r'CREATE TABLE (\w+)', self.sql_string, re.IGNORECASE)
        if match:
            return match.group(1)
        else:
            return "Invalid CREATE TABLE query"

    def is_valid_create_table_query(self) -> bool:
        """
        Validate if the SQL string is a valid CREATE TABLE query.
        
        Returns:
            bool: True if valid, otherwise False.
        """
        # Remove formatting
        clean_query = self.sql_string.replace("\n", " ").strip()

        pattern = r'^CREATE TABLE .+;\s*$'
        return bool(re.match(pattern, clean_query))
    
    def extract_sql_query_from_text(self) -> Optional[str]:
        """
        Extracts an SQL query from a given text.
        Useful when an LLM produces filler words/introductions when asked to generate SQL code.
        
        Returns:
            str or None: The SQL query if present, otherwise None.
        """
        match = re.findall(r'CREATE TABLE [^;]+;', self.sql_string)
        if match:
            # Extract only the last "CREATE TABLE" statement and add a space after "CREATE TABLE"
            last_statement = match[-1]
            return "CREATE TABLE " + last_statement.split("CREATE TABLE")[-1].strip()