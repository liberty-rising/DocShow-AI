from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from utils import call_hugging_face_api
import pandas as pd
from io import BytesIO

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World"}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Read only the first few lines into a DataFrame
    df = pd.read_csv(file.file, nrows=10)
    
    # Convert the DataFrame back to a CSV string
    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    sample_content = buffer.getvalue()
    
    result = call_hugging_face_api(sample_content)
    
    if result:
        return JSONResponse(content={"message": "File processed successfully", "result": result})
    else:
        return JSONResponse(content={"message": "Error processing file"}, status_code=400)

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}