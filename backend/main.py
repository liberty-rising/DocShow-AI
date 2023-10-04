from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from utils import call_llm_api, process_file

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World"}

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
    # Process file to string
    sample_content = process_file(file)
    
    result = call_llm_api(sample_content,msg,is_new_table)
    
    if result:
        return JSONResponse(content={"message": "File processed successfully", "result": result})
    else:
        return JSONResponse(content={"message": "Error processing file"}, status_code=400)

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}