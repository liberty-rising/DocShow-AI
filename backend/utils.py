from fastapi import FastAPI, File, UploadFile
from typing import Any

import requests

def api_request(prompt, url, headers):
    """Helper function to make an API request."""
    payload = json.dumps({"inputs": prompt})
    return requests.post(url, headers=headers, data=payload)

def call_hugging_face_api(file_content):
    hugging_face_url = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-70b-chat-hf"
    headers = {"Authorization": "Bearer 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"}

    response = requests.post(
        hugging_face_url,
        headers=headers,
        files={"file": file_content}
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def generate_create_table_statement(file_content, msg, hugging_face_url, headers):
    """
    Generates a SQL "CREATE TABLE" statement and description using Hugging Face API.

    Parameters:
        file_content (str): Sample data for the SQL statement.
        msg (str): Additional clarification for the table.
        hugging_face_url (str): Hugging Face API URL.
        headers (dict): API request headers.

    Returns:
        tuple: API responses for SQL statement and description.
    """
    
    sql_prompt = f"Create a SQL table statement for this sample data: {file_content}"
    sql_response = api_request(sql_prompt, hugging_face_url, headers)
    
    desc_prompt = "Create a brief description of the data in table."
    if msg:
        desc_prompt += f" Additional information: {msg}"
    desc_response = api_request(desc_prompt, hugging_face_url, headers)

    return sql_response, desc_response
    
def process_file(file: UploadFile, file_type: str) -> Any:
    """
    Process the uploaded file based on its type.

    Parameters:
        file (UploadFile): The uploaded file.
        file_type (str): The type of the uploaded file (e.g., 'csv', 'pdf', 'img').

    Returns:
        Any: Processed content of the file.
    """
    file_type = file_type.lower()

    if file_type == 'csv':
        df = pd.read_csv(file.file, nrows=10)
        buffer = BytesIO()
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