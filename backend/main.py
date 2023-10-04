from fastapi import FastAPI, File, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from utils import create_or_append_llm_table, process_file, save_to_data_lake

app = FastAPI()

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
        sample_content = process_file(file)
        
        # Call the LLM API
        llm_result = create_or_append_llm_table(sample_content, msg, is_new_table)

        # Optionally, save the file to a data lake
        save_to_data_lake(file)
    
        if llm_result:
            return JSONResponse(content={"message": "File processed successfully", "result": llm_result})
        else:
            raise HTTPException(status_code=400, detail="Error processing file with LLM API")
    
    except Exception as e:
        # General error handling
        return JSONResponse(content={"message": f"An error occured: {str(e)}"}, status_code=500)