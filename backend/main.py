from fastapi import FastAPI, File, Form, UploadFile, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from databases.chat_service import ChatHistoryService
from databases.database_managers import AppDatabaseManager, ClientDatabaseManager
from databases.sql_executor import SQLExecutor
from llms.base import BaseLLM
from llms.utils import ChatRequest, ChatResponse, get_llm_chat_object, get_llm_sql_object
from models import app_models, client_models
from routes.token import router as token_router
from security import get_current_user
from session_config import session_manager
from startup import run_startup_routines
from superset.superset_manager import SupersetManager
from superset.utils import get_superset_manager
from utils.table_manager import TableManager
from utils.utils import process_file, save_to_data_lake, get_app_logger


logger = get_app_logger(__name__)
logger.info("Logger initialised.")

app = FastAPI()

app.include_router(token_router)

# Initialize database managers
app_db_manager = AppDatabaseManager()
client_db_manager = ClientDatabaseManager()

# Create the tables in the databases
app_models.Base.metadata.create_all(bind=app_db_manager.engine) 
client_models.Base.metadata.create_all(bind=client_db_manager.engine)

# For DEV!!!
user_id = 1

@app.on_event("startup")
async def startup_event():
    run_startup_routines()

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
        processed_df, sample_content, header = process_file(file, encoding)

        # Instantiate TableManager
        table_manager = TableManager(llm)

        # Create new table if necessary
        if is_new_table:
            create_table_query = table_manager.create_table_with_llm(sample_content, header, extra_desc)
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

@app.get("/tables/")
async def get_tables():
    with ClientDatabaseManager() as session:
        executor = SQLExecutor(session)
        tables = executor.get_all_table_names_as_list()
    return tables

@app.post("/chat/")
async def chat_endpoint(request: ChatRequest, llm: BaseLLM = Depends(get_llm_chat_object)):
    user_input = request.user_input
    # Assume llm_chat is a function that sends user_input to your LLM and gets a response
    llm_output = llm.generate_text(user_input)
    return ChatResponse(llm_output=llm_output)

@app.delete("/chat_history/")
async def delete_chat_history():
    global user_id

    with ClientDatabaseManager() as session:
        chat_service = ChatHistoryService(session)
        chat_service.delete_chat_history(user_id)

    return {"message": "Chat history deleted"}

@app.delete("/table/")
async def drop_table(table_name: str):
    manager = TableManager()
    manager.drop_table(table_name)
    return {"message": f"Dropped table {table_name}"}

@app.get("/dashboards/")
async def list_dashboards(superset_manager: SupersetManager = Depends(get_superset_manager)):
    try:
        dashboards = superset_manager.list_dashboards()
        return {"dashboards": dashboards}
    except Exception as e:
        return {"error": str(e)}

@app.get("/dashboard/{dashboard_id}")
async def get_dashboard(dashboard_id: int, superset_manager: SupersetManager = Depends(get_superset_manager)):
    try:
        response = superset_manager.get_dashboard_by_id(dashboard_id)
        return response.text
    except Exception as e:
        return {"error": str(e)}

@app.get("/users/me/", response_model=app_models.UserOut)
async def read_users_me(current_user: app_models.User = Depends(get_current_user)):
    return current_user
    
@app.on_event("shutdown")
async def shutdown_event():
    # Close all sessions
    for user_id in session_manager.sessions.keys():
        session_manager.close_session(user_id)