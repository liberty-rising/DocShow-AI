from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from utils.utils import process_file, save_to_data_lake

from backend.models import app_models, client_models
from backend.databases import app_db_config, client_db_config
from backend.llms.base import BaseLLM
from backend.llms.gpt import GPTLLM
from backend.utils.table_manager import TableManager

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

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...), extra_desc: str = "", is_new_table: bool = False, llm: BaseLLM = Depends(get_llm_sql_object)):
    """
    Upload a file and optionally include a message to clarify user data for the LLM.

    Parameters:
        file (UploadFile, required): The file to be uploaded and processed.
        extra_desc (str, optional): An optional message sent to the LLM to clarify the data from the user.
        is_new_table (bool, optional): Indicates whether the table is new. Defaults to False.
        llm (BaseLLM, required): An instance of a Language Learning Model (LLM), obtained through dependency injection. Responsible for generating the SQL table.

    Returns:
        JSONResponse: A JSON response containing either a success message and result or an error message.
    """
    try:
        # Process the file to get the sample content
        processed_file, sample_content = process_file(file)

        # Instatiate TableManager
        table_manager = TableManager(database="client", llm=llm)

        # Create new table if necessary
        if is_new_table:
            create_table_query = table_manager.create_table_with_llm(sample_content, extra_desc)
            table_manager.create_table_desc_with_llm(create_table_query, sample_content, extra_desc)
        
        # Append file to table
        table_name = table_manager.determine_table(sample_content, extra_desc)
        table_manager.append_to_table(processed_file, table_name)

        # Optionally, save the file to a data lake
        save_to_data_lake(file)
    
        return JSONResponse(content={"message": "File processed successfully"}, status_code=200)
        
    except HTTPException as e:
        # Specific error handling for HTTP exceptions
        return JSONResponse(content={"message": f"HTTP Exception: {e.detail}"}, status_code=e.status_code)
    
    except Exception as e:
        # General error handling
        return JSONResponse(content={"message": f"An error occured: {str(e)}"}, status_code=500)