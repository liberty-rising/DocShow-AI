from fastapi import FastAPI, File, UploadFile
from io import StringIO
from typing import Any

import json
import pandas as pd
import requests

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

def call_llm_api(file_content, msg, is_new_table):
    llm_url = "https://api.runpod.ai/v2/2btspg14jnwza1/runsync"
    headers = {
        "Authorization": "Bearer 05IB5U9J6DD7UG8GXO0X1DU2M68JF5AZODD5JC1J",
        "Content-Type": "application/json"}

    if is_new_table:
        sql_response = generate_create_table_statement(file_content,msg,llm_url,headers)
    
    print("SQL: ",sql_response.json())
    return None
    # if response.status_code == 200:
    #     return response.json()
    # else:
    #     return None
    
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
    sql_context = f"You are specialized in generating SQL table creation statements based on\
          provided sample data. Ensure the statements are correctly formatted and adhere to SQL syntax standards.\
          Only provide the SQL response, nothing else. Do not acknowledge the questions or tasks in your answer."
    sql_prompt = f"Create a SQL table statement for this sample data: {file_content}"
    if msg:
        sql_prompt += f" Additional information about data: {msg}"
    full_prompt = prompt_format(sql_context,sql_prompt)

    sql_response = api_request(full_prompt,llm_url,headers)

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

    if file_type == 'csv':
        df = pd.read_csv(file.file, nrows=10)
        buffer = StringIO()
        df.to_csv(buffer, index=False)
        return buffer.getvalue()
    elif file_type == 'pdf':
        # PDF processing logic here
        pass
    elif file_type in ['img','jpg','jpeg','png']:
        # Image processing logic here
        pass
    else:
        raise ValueError("Unsupported file type")
    

def prompt_format(context: str, prompt: str):
    full_prompt = f"""[INST] <<SYS>>{context}<</SYS>>{prompt}[/INST]"""
    return full_prompt