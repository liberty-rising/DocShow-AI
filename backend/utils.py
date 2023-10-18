from fastapi import File, HTTPException, UploadFile
from io import StringIO
from typing import Any, Dict, Tuple, Union

from backend.databases.db_utils import ClientDatabaseManager, SQLExecutor, SQLStringManipulator, TableMetadataManager
from backend.llms.base import BaseLLM

import pandas as pd


def create_llm_table(sample_file_content: str, msg: str, llm: BaseLLM) -> str:
    """
    Creates a table using an LLM based on sample file content and a message.

    Parameters:
    - sample_file_content (str): The sample file content used to create the table.
    - msg (str): Additional message to give context to LLM for table creation.
    - llm (BaseLLM): The language learning model used for generating SQL statements.

    Returns:
    - create_query: str containing the SQL create table query if successful, None otherwise.
    """
    try:
        with ClientDatabaseManager() as conn:
            sql_executor = SQLExecutor(conn)
            table_names = sql_executor.get_all_table_names()
            
        raw_create_query = llm.generate_create_statement(sample_file_content,msg,table_names)

        create_query = SQLStringManipulator(raw_create_query).extract_sql_query_from_text()  # Just in case

        if SQLStringManipulator(create_query).is_valid_create_table_query():  # Checks if the query is valid
            with ClientDatabaseManager() as conn:
                sql_executor = SQLExecutor(conn)
                sql_executor.execute_create_query(create_query)
            return create_query
    except Exception as e:
        # Log the error message here
        print(f"An error occurred while creating the table: {str(e)}")
        return None

def create_table_desc(create_query: str, sample_file_content: str, extra_desc: str, llm: BaseLLM) -> Union[Dict, None]:
    """
    Fetches and stores the description of a table created in LLM based on the CREATE TABLE query,
    sample file content, and a message.

    Parameters:
    - create_query (str): The CREATE TABLE query used to create the table.
    - sample_file_content (str): Sample file content used in table creation.
    - extra_desc (str): Additional message to give context to LLM for generating the table description.
    - llm (BaseLLM)

    Returns:
    - Union[Dict, None]: JSON response containing table description if successful, None otherwise.
    """

    try:
        # API call to generate and fetch table description
        description = llm.generate_table_desc(create_query, sample_file_content, extra_desc)
        
        table_name = SQLStringManipulator(create_query).get_table_from_create_query()
        
        # Store description in separate table
        with TableMetadataManager(database="client") as manager:
            manager.store_table_desc(table_name, create_query, description)

    except Exception as e:
        # Log the error message here
        print(f"An error occurred while fetching table description: {str(e)}")
        return None

def handle_table_creation(sample_file_content, msg, llm):
    create_query = create_llm_table(sample_file_content, msg, llm)
    create_table_desc(create_query, sample_file_content, msg, llm)

def determine_and_append_to_table(processed_file: UploadFile, sample_content: str, extra_desc: str, llm: BaseLLM):
    """
    Determines the appropriate table based on sample data and a message, then appends the uploaded file to that table.
    Uses ClientDatabaseManager for database connection and SQLExecutor for SQL operations.

    Parameters:
    - processed_file (UploadFile): The uploaded file to be appended.
    - sample_content (str): The sample content for table determination.
    - extra_desc (str): Additional metadata or instructions.
    - llm (BaseLLM): An instance of a language learning model.

    Side-effects:
    - Appends data to the table determined by the LLM.
    - Raises an HTTPException if the table name cannot be determined.
    """
    with TableMetadataManager(database="client") as manager:
        table_metadata = manager.get_metadata()
        formatted_table_metadata = manager.format_table_metadata_for_llm(table_metadata)

    table_name = llm.fetch_table_from_sample(sample_content, extra_desc, formatted_table_metadata)

    if table_name:
        with ClientDatabaseManager() as conn:
            sql_executor = SQLExecutor(conn)
            sql_executor.append_csv_to_table(processed_file, table_name)
    else:
        raise HTTPException(status_code=400, detail="Could not determine table name")
    
def process_file(file: UploadFile) -> Any:
    """
    Process the uploaded file based on its type.

    Parameters:
        file (UploadFile): The uploaded file.

    Returns:
        Any: Processed content of the file.
    """
    # Find file type by file extension
    file_name = file.filename
    file_type = file_name.split(".")[-1].lower()

    files = {"processed_file": None, "sample_file_content": None}

    if file_type == 'csv':
        df = pd.read_csv(file.file, nrows=10)
        buffer = StringIO()
        df.to_csv(buffer, index=False)

        files["processed_file"] = file
        files["sample_file_content"] = buffer.getvalue()

    elif file_type == 'pdf':
        # PDF processing logic here
        pass
    elif file_type in ['img','jpg','jpeg','png']:
        # Image processing logic here
        pass
    else:
        raise ValueError("Unsupported file type")
    
    return files["processed_file"], files["sample_file_content"]

def save_to_data_lake(file: UploadFile = File(...)):
    pass