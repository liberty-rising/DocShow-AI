from api_utils import api_request_llm, get_llm_api_credentials, poll_for_llm_task_completion
from sql_utils import get_table_names

from typing import Dict, Union

def generate_create_table_statement(file_content, msg):
    """
    Generates a SQL "CREATE TABLE" statement and description using provided LLM API.

    Parameters:
        file_content (str): Sample data for the SQL statement.
        msg (str): Additional clarification for the table.

    Returns:
        tuple: API responses for SQL statement and description.
    """
    llm_url,headers = get_llm_api_credentials()

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

def generate_table_desc(create_query: str, sample_file_content: str, msg: str) -> Union[Dict, None]:
    """
    Generates and fetches a table description based on a CREATE TABLE query,
    sample file content, and a message using the LLM API.

    Parameters:
    - create_query (str): The CREATE TABLE query used to create the table.
    - sample_file_content (str): Sample file content for the table.
    - msg (str): Additional message for clarification or other purposes.

    Returns:
    - Union[Dict, None]: JSON response containing table description if successful, None otherwise.
    """
    llm_url, headers = get_llm_api_credentials()

    desc_context = "Generate a description of the table based on the SQL CREATE TABLE query. Do not include any additional text, explanations, or filler words."
    desc_prompt = f"Generate a description for the table created using the following SQL CREATE TABLE query: {create_query}. \
        Here is a sample of the data: {sample_file_content}"
    
    if msg:
        desc_prompt += f" Additional information about the data: {msg}"

    full_prompt = prompt_format(desc_context,desc_prompt)

    desc_response = api_request_llm(full_prompt, llm_url, headers)

    task_id = desc_response.json().get('id')

    # Poll for task completion
    desc_response = poll_for_llm_task_completion(task_id, headers)

    return desc_response

def prompt_format(context: str, prompt: str):
    full_prompt = f"""[INST] <<SYS>>{context}<</SYS>>{prompt}[/INST]"""
    return full_prompt