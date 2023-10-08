from fastapi import FastAPI, File, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from utils import append_llm_table, get_table_name, handle_table_creation, process_file, save_to_data_lake

from models import app_models, client_models
from database import app_db_config, client_db_config

app = FastAPI()

# Create the tables in the databases
app_models.Base.metadata.create_all(bind=app_db_config.engine)
client_models.Base.metadata.create_all(bind=client_db_config.engine)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...), msg: str = "", is_new_table: bool = False):
    """
    Upload a file and optionally include a message to clarify user data for the LLM.

    Parameters:
        file (UploadFile, required): The file to be uploaded and processed.
        msg (str, optional): An optional message sent to the LLM to clarify the data from the user.
        is_new_table (bool, optional): Indicates whether the table is new. Defaults to False.

    Returns:
        JSONResponse: A JSON response containing either a success message and result or an error message.
    """
    try:
        # Process the file to get the sample content
        processed_file, sample_file_content = process_file(file)

        # Create new table if necessary
        if is_new_table:
            handle_table_creation(sample_file_content, msg)
        
        # Append file to table
        table_name = get_table_name(sample_file_content, msg)
        llm_append_result = append_llm_table(processed_file, msg, table_name)

        # Optionally, save the file to a data lake
        save_to_data_lake(file)
    
        return JSONResponse(content={"message": "File processed successfully"}, status_code=200)
        
    except HTTPException as e:
        # Specific error handling for HTTP exceptions
        return JSONResponse(content={"message": f"HTTP Exception: {e.detail}"}, status_code=e.status_code)
    
    except Exception as e:
        # General error handling
        return JSONResponse(content={"message": f"An error occured: {str(e)}"}, status_code=500)