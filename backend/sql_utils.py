"""
This module contains utility functions for interacting with SQL databases.
It includes functions for creating, reading, updating, and deleting records,
as well as other database operations.
"""
from databases.client_db_config import SessionLocal
from models.client_models import TableMetadata

from fastapi import HTTPException, UploadFile
from typing import List
import csv
import re
import sqlite3

def append_to_table(processed_file: UploadFile, table_name: str):
    """
    Appends the content of an uploaded CSV file to a specified table in the database.

    Parameters:
    - processed_file (UploadFile): The uploaded file to be appended.
    - table_name (str): The name of the table to which the file will be appended.

    Side-effects:
    - Updates the database table with new rows from the processed_file.
    - Logs an error message to the console if the operation fails.
    """
    try:
        # Initialize the connection to SQLite database
        conn = sqlite3.connect("client_database.db")
        cursor = conn.cursor()

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
        conn.commit()

    except Exception as e:
        print(f"An error occurred while appending data to table {table_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        conn.close()

def execute_sql_create_query(query: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def extract_sql_query(text):
    """
    Created due to limited capability of Llama-2-13B-chat-GPTQ being able to return pure sql without extra words.
    """
    match = re.findall(r'CREATE TABLE [^;]+;', text)
    if match:
        # Extract only the last "CREATE TABLE" statement and add a space after "CREATE TABLE"
        last_statement = match[-1]
        return "CREATE TABLE " + last_statement.split("CREATE TABLE")[-1].strip()

def get_db_path() -> str:
    return "client_database.db"

def get_table_from_create_query(create_query: str):
    """
    Extract the table name from a SQL CREATE TABLE query.

    Parameters:
    create_query (str): The SQL CREATE TABLE query.

    Returns:
    str: The table name.
    """
    # Use regular expression to extract table name
    match = re.search(r'CREATE TABLE (\w+)', create_query, re.IGNORECASE)
    if match:
        return match.group(1)
    else:
        return "Invalid CREATE TABLE query"
    
def get_table_metadata() -> List[TableMetadata]:
    """
    Fetches all rows from the table_metadata database table.

    Returns:
    - List[TableMetadata]: A list of TableMetadata objects representing each row in the table_metadata table.

    Raises:
    - HTTPException: An exception with a 500 status code if a database error occurs.
    """
    db = SessionLocal()
    try:
        return db.query(TableMetadata).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        db.close()

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

def get_table_names() -> str:
    """Get names of all tables in database."""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

    tables = cursor.fetchall()
    table_names = [table[0] for table in tables]
    
    conn.close()

    table_names_str = ', '.join(table_names)
    
    return table_names_str

def is_valid_create_table_query(query: str) -> bool:
    # Remove formatting
    clean_query = query.replace("\n", " ").strip()

    pattern = r'^CREATE TABLE .+;\s*$'
    return bool(re.match(pattern, clean_query))

def store_table_desc(table_name: str, create_query: str, description: str):
    """
    Store the table name and its description in a database table called 'table_metadata'.

    Parameters:
    table_name (str): The name of the table to describe.
    create_query (str): The CREATE TABLE statement for the table.
    description (str): The description of the table.
    """
    # Initialize the database session manually
    db = SessionLocal()

    try:
        # Your database operations here
        table_metadata = TableMetadata(table_name=table_name, create_statement=create_query, description=description)
        db.merge(table_metadata)
        db.commit()
    finally:
        db.close()
