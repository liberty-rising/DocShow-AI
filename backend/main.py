import logging

from fastapi import FastAPI, File, Form, UploadFile, Depends
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from utils.utils import process_file, save_to_data_lake

from models import app_models, client_models
from databases import app_db_config, client_db_config
from llms.base import BaseLLM
from llms.gpt import GPTLLM
from llms.utils import ChatRequest, ChatResponse
from utils.table_manager import TableManager

app = FastAPI()

# Create the tables in the databases
app_models.Base.metadata.create_all(bind=app_db_config.engine)
client_models.Base.metadata.create_all(bind=client_db_config.engine)

def get_llm_sql_object():
    # TODO: Pull LLM SQL history from db and initialise object
    # history = get_llm_sql_history_for_user
    history = [] # Temporary

    # Initialize LLM object
    llm = GPTLLM(history)
    return llm

def get_llm_chat_object():
    # TODO: Pull LLM SQL history from db and initialise object
    # history = get_llm_chat_history_for_user
    history = [] # Temporary

    # Initialize LLM object
    llm = GPTLLM(history)
    return llm

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...), extra_desc: str = Form(default=""), is_new_table: bool = Form(default=False), encoding: str = Form(default=""), llm: BaseLLM = Depends(get_llm_sql_object)):
    """
    Upload a file and optionally include a message to clarify user data for the LLM.

    Parameters:
        file (UploadFile, required): The file to be uploaded and processed.
        extra_desc (str, optional): An optional message sent to the LLM to clarify the data from the user.
        is_new_table (bool, optional): Indicates whether the table is new. Defaults to False.
        encoding (str, optional): Indicates the encoding of the file. Useful for CSVs.
        llm (BaseLLM, required): An instance of a Language Learning Model (LLM), obtained through dependency injection. Responsible for generating the SQL table.

    Returns:
        JSONResponse: A JSON response containing either a success message and result or an error message.
    """
    try:
        # Process the file to get the sample content
        processed_df, sample_content = process_file(file, encoding, is_header=True)

        # Instantiate TableManager
        table_manager = TableManager(database="client", llm=llm)

        # Create new table if necessary
        if is_new_table:
            create_table_query = table_manager.create_table_with_llm(sample_content, extra_desc)
            table_manager.create_table_desc_with_llm(create_table_query, sample_content, extra_desc)
        
        # Append file to table
        table_name = table_manager.determine_table(sample_content, extra_desc)
        table_manager.append_to_table(processed_df, table_name)

        # Optionally, save the file to a data lake
        save_to_data_lake(file)
    
        return JSONResponse(content={"message": "File processed successfully"}, status_code=200)
        
    except HTTPException as e:
        # Specific error handling for HTTP exceptions
        return JSONResponse(content={"message": f"HTTP Exception: {e.detail}"}, status_code=e.status_code)
    
    except Exception as e:
        # General error handling
        return JSONResponse(content={"message": f"An error occured: {str(e)}"}, status_code=500)

@app.get("/encodings/")
async def get_encodings(file_type: str = ""):
    encodings = {
        "csv":["utf_8","ascii","latin_1","utf_16","ANSI"],
        "pdf":[]
    }
    return encodings.get("csv",None)

@app.get("/file_types/")
async def get_file_types():
    return ["csv"]

@app.post("/chat/")
async def chat_endpoint(request: ChatRequest, llm: BaseLLM = Depends(get_llm_chat_object)):
    user_input = request.user_input
    # Assume llm_chat is a function that sends user_input to your LLM and gets a response
    model_output = llm.generate_text(user_input)
    return ChatResponse(model_output=model_output)