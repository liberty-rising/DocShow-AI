from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.database_manager import DatabaseManager
from models.base import Base
from routes.auth_routes import auth_router
from routes.chat_routes import chat_router
from routes.chart_routes import chart_router
from routes.dashboard_routes import dashboard_router
from routes.data_profile_routes import data_profile_router
from routes.file_routes import file_router
from routes.organization_routes import organization_router
from routes.table_routes import table_router
from routes.user_routes import user_router
from settings import APP_ENV
from startup import run_startup_routines
from utils.utils import get_app_logger


logger = get_app_logger(__name__)
logger.info("Logger initialised.")

app = FastAPI()

if APP_ENV == "prod":
    origins = ["https://docshow.ai"]
else:
    origins = ["https://127.0.0.1"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
app.include_router(data_profile_router)
app.include_router(file_router)
app.include_router(organization_router)
app.include_router(table_router)
app.include_router(user_router)

# Initialize database manager
db_manager = DatabaseManager()

# Create the tables in the databases
Base.metadata.create_all(bind=db_manager.engine)
