from fastapi import FastAPI, File, UploadFile
from io import StringIO
from typing import Any, Dict, Union
from .api_utils import api_request_llm, get_llm_api_credentials, poll_for_llm_task_completion
from .sql_utils import execute_sql_create_query, extract_sql_query, get_table_names, is_valid_create_table_query 

import json
import pandas as pd
import re
import requests
import sqlite3
import time


def create_llm_table(sample_file_content: str, msg: str):
    """
    Creates a table using an LLM. The table is based on sample file content and a message.

    Parameters:
    - sample_file_content (str): The sample file content used to create the table.
    - msg (str): Additional message to log or use in table creation.

    Returns:
    - Union[Dict, None]: JSON response if successful, None otherwise.
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
                    return sql_response.json()
                
                
            print("Retrying...")
            time.sleep(retry_delay)
                
        raise Exception("Can't create CREATE TABLE statement.")
    
    except Exception as e:
        # Log the error message here
        print(f"An error occurred: {str(e)}")
        return None

def append_llm_table(processed_file: UploadFile = File(...), msg: str = ""):
    # Code for appending data to existing tables
    pass
    
def generate_create_table_statement(file_content, msg, llm_url, headers):
    """
    Generates a SQL "CREATE TABLE" statement and description using provided LLM API.

    Parameters:
        file_content (str): Sample data for the SQL statement.
        msg (str): Additional clarification for the table.
        llm_url (str): LLM API URL.
        headers (dict): API request headers.

    Returns:
        tuple: API responses for SQL statement and description.
    """
    table_names = get_table_names()
    sql_context = "Generate only a SQL CREATE TABLE statement based on the provided sample data. Do not include any additional text, explanations, or filler words."
    sql_prompt = f"Generate SQL CREATE TABLE statement for the following sample data: {file_content}.\
        Do not include any additional text, explanations, or filler words.\
        Do not use the following table names as they are already in use: {table_names}"

    if msg:
        sql_prompt += f" Additional information about data: {msg}"
    full_prompt = prompt_format(sql_context,sql_prompt)

    sql_response = api_request_llm(full_prompt,llm_url,headers)

    task_id = sql_response.json().get('id')

    # Poll for task completion
    sql_response = poll_for_llm_task_completion(task_id,headers)

    return sql_response
    
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

def prompt_format(context: str, prompt: str):
    full_prompt = f"""[INST] <<SYS>>{context}<</SYS>>{prompt}[/INST]"""
    return full_prompt

def save_to_data_lake(file: UploadFile = File(...)):
    pass