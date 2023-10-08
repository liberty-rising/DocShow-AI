from sql_utils import append_to_table

from fastapi import File, HTTPException, UploadFile
from io import StringIO
from typing import Any, Dict, Tuple, Union
from llm_utils import generate_create_table_statement, generate_table_desc, fetch_llm_table_from_sample
from sql_utils import execute_sql_create_query, extract_sql_query, get_table_from_create_query, is_valid_create_table_query, store_table_desc

import pandas as pd
import time


def determine_and_append_to_table(processed_file: UploadFile, sample_file_content: str, msg: str):
    """
    Determines the appropriate table based on sample data and a message, and then appends the uploaded file to that table.

    Parameters:
    - processed_file (UploadFile): The uploaded file to be appended.
    - sample_file_content (str): The sample file content to analyze.
    - msg (str): Additional metadata or instructions.

    Side-effects:
    - Calls append_to_table function to append data to the determined table.
    - Raises an HTTPException if the table name cannot be determined.
    """
    table_name = get_table_name(sample_file_content, msg)
    print(table_name)
    return

    if table_name is None:
        raise HTTPException(status_code=400, detail="Could not determine table name")
    
    try:
        append_to_table(processed_file, table_name)
    except Exception as e:
        print(f"An error occurred while appending data to table {table_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

def create_llm_table(sample_file_content: str, msg: str) -> Union[Tuple[Dict, str], None]:
    """
    Creates a table using an LLM. The table is based on sample file content and a message.

    Parameters:
    - sample_file_content (str): The sample file content used to create the table.
    - msg (str): Additional message to give context to LLM for table creation.

    Returns:
    - Union[Tuple[Dict, str], None]: Tuple containing the JSON response and SQL query if successful, None otherwise.
    """
    max_retries = 3
    retry_delay = 2  # seconds

    try:
        for _ in range(max_retries):
            sql_response = generate_create_table_statement(sample_file_content,msg)
                
            if sql_response.status_code == 200:
                sql_query = extract_sql_query(sql_response.json()["output"])

                if is_valid_create_table_query(sql_query):
                    execute_sql_create_query(sql_query)
                    return sql_response.json(), sql_query
                
                
            print("Retrying...")
            time.sleep(retry_delay)
                
        raise Exception("Can't create CREATE TABLE statement.")
    
    except Exception as e:
        # Log the error message here
        print(f"An error occurred: {str(e)}")
        return None

def create_table_desc(create_query: str, sample_file_content: str, msg: str) -> Union[Dict, None]:
    """
    Fetches and stores the description of a table created in LLM based on the CREATE TABLE query,
    sample file content, and a message.

    Parameters:
    - create_query (str): The CREATE TABLE query used to create the table.
    - sample_file_content (str): Sample file content used in table creation.
    - msg (str): Additional message to give context to LLM for generating the table description.

    Returns:
    - Union[Dict, None]: JSON response containing table description if successful, None otherwise.
    """

    try:
        # API call to generate and fetch table description
        description_response = generate_table_desc(create_query, sample_file_content, msg)

        if description_response.status_code == 200:
            table_name = get_table_from_create_query(create_query)
            description = description_response.json()['output']
            
            # Store description in separate table
            store_table_desc(table_name,create_query,description)

            return description_response

    except Exception as e:
        # Log the error message here
        print(f"An error occurred while fetching table description: {str(e)}")
        return None

def get_table_name(sample_file_content: str, msg: str) -> str:
    """
    Fetches the appropriate table name for the sample data using an API call to an LLM.
    
    Parameters:
    - sample_file_content (str): The sample file content to analyze.
    - msg (str): Additional metadata or instructions.

    Returns:
    - str: The predicted table name, or None if an error occurs.

    Side-effects:
    - Logs an error message to the console if the table name cannot be fetched.
    """
    try:
        table_response = fetch_llm_table_from_sample(sample_file_content, msg)
        return table_response.json()['output']
    except Exception as e:
        print(f"An error occurred while fetching table name: {str(e)}")
        return None

def handle_table_creation(sample_file_content, msg):
    table_response, create_query = create_llm_table(sample_file_content, msg)
    desc_response = create_table_desc(create_query, sample_file_content, msg)
    
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