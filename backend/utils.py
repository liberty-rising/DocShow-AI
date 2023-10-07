from fastapi import File, UploadFile
from io import StringIO
from typing import Any, Dict, Tuple, Union
from .api_utils import get_llm_api_credentials
from .llm_utils import generate_create_table_statement, generate_table_desc
from .sql_utils import execute_sql_create_query, extract_sql_query, get_table_from_create_query, is_valid_create_table_query, store_table_desc

import pandas as pd
import time


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
        llm_url,headers = get_llm_api_credentials()

        for _ in range(max_retries):
            sql_response = generate_create_table_statement(sample_file_content,msg,llm_url,headers)
                
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
        # Assume get_llm_api_credentials() returns the LLM API URL and headers
        llm_url, headers = get_llm_api_credentials()

        # Replace this with actual API call to generate and fetch table description
        description_response = generate_table_desc(create_query, sample_file_content, msg, llm_url, headers)

        if description_response.status_code == 200:
            table_name = get_table_from_create_query(create_query)
            description = description_response.json()['output']
            
            # Store description in separate table
            store_table_desc(table_name,description)

            return description_response

    except Exception as e:
        # Log the error message here
        print(f"An error occurred while fetching table description: {str(e)}")
        return None

def append_llm_table(processed_file: UploadFile, msg: str, table_name: str):
    # Code for appending data to existing tables
    pass
    
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