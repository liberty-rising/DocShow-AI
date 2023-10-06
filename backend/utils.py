from fastapi import FastAPI, File, UploadFile
from io import StringIO
from typing import Any

import json
import pandas as pd
import re
import requests
import sqlite3
import time

def api_request(prompt, url, headers):
    """Helper function to make an API request."""
    payload = json.dumps(
        {
            "input": {
                "prompt": prompt,
                "max_new_tokens": 500,
                "temperature":0.7,
                "top_k":50,
                "top_p":0.7,
                "repetition_penalty":1.2,
                "batch_size": 8,
                "stop": ["</s>"]}
        })
    return requests.post(url, headers=headers, data=payload)

def create_llm_table(sample_file_content: str, msg: str):
    max_retries = 3
    retry_delay = 2  # 2 seconds

    try:
        llm_url,headers = get_api_credentials()

        for _ in range(max_retries):
            sql_response = generate_create_table_statement(sample_file_content,msg,llm_url,headers)
                
            if sql_response.status_code == 200:
                print("SQL",sql_response.json())
                sql_query = extract_sql_query(sql_response.json()["output"])
                print(f"SQL Query: {sql_query}")

                if is_valid_create_table_query(sql_query):
                    execute_sql_create_query(sql_query)
                    return sql_response.json()
                
                else:
                    print("Retrying...")
                    time.sleep(retry_delay)
                
        raise Exception("Can't create CREATE TABLE statement.")
    
    except Exception as e:
        # Log the error message here
        print(f"An error occurred: {str(e)}")
        return None

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

def append_llm_table(processed_file: UploadFile = File(...), msg: str = ""):
    # Code for appending data to existing tables
    pass
    

def get_api_credentials():
    llm_url = "https://api.runpod.ai/v2/2btspg14jnwza1/runsync"
    headers = {
        "Authorization": "Bearer 05IB5U9J6DD7UG8GXO0X1DU2M68JF5AZODD5JC1J",
        "Content-Type": "application/json"}
    return llm_url, headers
    
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

    sql_response = api_request(full_prompt,llm_url,headers)

    task_id = sql_response.json().get('id')

    # Poll for task completion
    while True:
        sql_response = requests.get(f"https://api.runpod.ai/v2/2btspg14jnwza1/status/{task_id}", headers=headers)
        if sql_response.json().get('status') == 'COMPLETED':
            break
        time.sleep(1)  # Wait for a second before polling again

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

def get_db_path() -> str:
    return "client_database.db"

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

def extract_sql_query(text):
    """
    Created due to limited capability of Llama-2-13B-chat-GPTQ being able to return pure sql without extra words.
    """
    match = re.findall(r'CREATE TABLE [^;]+;', text)
    if match:
        # Extract only the last "CREATE TABLE" statement and add a space after "CREATE TABLE"
        last_statement = match[-1]
        return "CREATE TABLE " + last_statement.split("CREATE TABLE")[-1].strip()
    
    
def save_to_data_lake(file: UploadFile = File(...)):
    pass

def is_valid_create_table_query(query: str) -> bool:
    # Remove formatting
    clean_query = query.replace("\n", " ").strip()

    pattern = r'^CREATE TABLE .+;\s*$'
    return bool(re.match(pattern, clean_query))