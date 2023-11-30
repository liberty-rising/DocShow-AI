from fastapi import FastAPI

from databases.database_managers import AppDatabaseManager, ClientDatabaseManager
from models.app.base import Base as AppBase
from models.client.base import Base as ClientBase
from routes.auth_routes import auth_router
from routes.chat_routes import chat_router
from routes.chart_routes import chart_router
from routes.dashboard_routes import dashboard_router
from routes.file_routes import file_router
from routes.organization_routes import organization_router
from routes.table_routes import table_router
from routes.user_routes import user_router
# from session_config import session_manager
from startup import run_startup_routines
from utils.utils import get_app_logger


logger = get_app_logger(__name__)
logger.info("Logger initialised.")

app = FastAPI()

async def startup_event():
    run_startup_routines()

async def shutdown_event():
    pass

# Registering the startup and shutdown events
app.router.on_startup.append(startup_event)
app.router.on_shutdown.append(shutdown_event)

# Add routers
app.include_router(auth_router)
app.include_router(chart_router)
app.include_router(chat_router)
app.include_router(dashboard_router)
app.include_router(file_router)
app.include_router(organization_router)
app.include_router(table_router)
app.include_router(user_router)

# Initialize database managers
app_db_manager = AppDatabaseManager()
client_db_manager = ClientDatabaseManager()

# Create the tables in the databases
AppBase.metadata.create_all(bind=app_db_manager.engine) 
ClientBase.metadata.create_all(bind=client_db_manager.engine)
