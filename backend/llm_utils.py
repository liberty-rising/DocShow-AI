from models.client_models import TableMetadata

from api_utils import api_request_llm, get_llm_api_credentials, poll_for_llm_task_completion
from sql_utils import get_table_metadata, get_table_names

from typing import Dict, List, Union


def fetch_llm_table_from_sample(sample_file_content: str, msg: str) -> Union[Dict, None]:
    """
    Fetches the appropriate table name from an LLM based on the sample data and existing table metadata.
    
    Parameters:
    - sample_file_content (str): The sample file content to analyze.
    - msg (str): Additional metadata or instructions.

    Returns:
    - Union[Dict, None]: JSON response containing predicted table name if successful, None otherwise.
    """
    llm_url, headers = get_llm_api_credentials()

    # Get and format existing table metadata
    table_metadata_rows = get_table_metadata()
    formatted_metadata = format_table_metadata_for_llm(table_metadata_rows)

    context = "Based on the sample data and existing table metadata, determine to which table the sample data should be appended."
    prompt = f"Sample Data: {sample_file_content}\n\nExisting Table Metadata:\n{formatted_metadata}"

    if msg:
        prompt += f"\n\nAdditional information about the sample data: {msg}"

    full_prompt = prompt_format(context, prompt)

    # Make an API request to the LLM
    table_response = api_request_llm(full_prompt, llm_url, headers)
    task_id = table_response.json().get('id')

    # Poll for task completion
    table_response = poll_for_llm_task_completion(task_id, headers)

    return table_response

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
        sql_prompt += f"Additional information about the sample data: {msg}"
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
    desc_prompt = f"""
        Generate a comprehensive description for the table that will be created using the SQL CREATE TABLE query below. 
        This description should help in:
        1. Categorizing new data into this table or instead to other existing tables.
        2. Providing the context needed to generate suggested queries for reports and analytics in the future.

        SQL CREATE TABLE Query:
        {create_query}

        Sample Data:
        {sample_file_content}
        """
    
    if msg:
        desc_prompt += f"Additional information about the sample data: {msg}"

    full_prompt = prompt_format(desc_context,desc_prompt)

    desc_response = api_request_llm(full_prompt, llm_url, headers)

    task_id = desc_response.json().get('id')

    # Poll for task completion
    desc_response = poll_for_llm_task_completion(task_id, headers)

    return desc_response

def prompt_format(context: str, prompt: str):
    full_prompt = f"""[INST] <<SYS>>{context}<</SYS>>{prompt}[/INST]"""
    return full_prompt