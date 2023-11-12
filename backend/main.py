from fastapi import FastAPI

from databases.database_managers import AppDatabaseManager, ClientDatabaseManager
from models import app_models, client_models
from routes.chat_routes import chat_router
from routes.file_routes import file_router
from routes.superset_routes import superset_router
from routes.table_routes import table_router
from routes.token import router as token_router
from routes.user_routes import user_router
from session_config import session_manager
from startup import run_startup_routines
from utils.utils import get_app_logger


logger = get_app_logger(__name__)
logger.info("Logger initialised.")

app = FastAPI()

app.include_router(chat_router)
app.include_router(file_router)
app.include_router(superset_router)
app.include_router(table_router)
app.include_router(token_router)
app.include_router(user_router)

# Initialize database managers
app_db_manager = AppDatabaseManager()
client_db_manager = ClientDatabaseManager()

# Create the tables in the databases
app_models.Base.metadata.create_all(bind=app_db_manager.engine) 
client_models.Base.metadata.create_all(bind=client_db_manager.engine)

@app.on_event("startup")
async def startup_event():
    run_startup_routines()
    
@app.on_event("shutdown")
async def shutdown_event():
    # Close all sessions
    for user_id in session_manager.sessions.keys():
        session_manager.close_session(user_id)