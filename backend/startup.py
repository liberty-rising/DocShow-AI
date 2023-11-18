"""
Startup Module

This module contains functions that are executed during the startup of the application.
It checks the configuration settings and seeds the database when running in a development environment.

Usage:
    >>> from startup import run_startup_routines
    >>> run_startup_routines()
"""
from databases.database_managers import AppDatabaseManager, ClientDatabaseManager
from databases.dashboard_manager import DashboardManager
from databases.user_manager import UserManager
from envs.dev.utils import seed_client_db
from models.app_models import User
from models.client_models import Dashboard
from security import get_password_hash
from settings import APP_ENV, JWT_SECRET_KEY
from utils.utils import get_app_logger


logger = get_app_logger(__name__)

def run_startup_routines():
    check_jwt_secret_key()

    if APP_ENV == 'development':
        create_admin_user()
        create_sample_dashboard()
        seed_client_db()

def check_jwt_secret_key():
    if APP_ENV != 'development' and JWT_SECRET_KEY == 'mysecretkey':
        raise EnvironmentError("JWT_SECRET_KEY must be set in non-development environments")

def create_admin_user():
    """Creates an admin user if it doesn't already exist."""
    admin_user = User(
        username = 'admin',
        hashed_password = get_password_hash('admin'),
        email = 'admin@docshow.ai',
        organization = 'DocShow AI',
        role = 'admin'
    )

    with AppDatabaseManager() as session:
        user_manager = UserManager(session)
        existing_user = user_manager.get_user(admin_user.username)
        if not existing_user:
            user_manager.create_user(admin_user)
            logger.debug("Admin user created.")
        else:
            logger.debug("Admin user already exists.")

def create_sample_dashboard():
    dashboard = Dashboard(
        name = "Sample Dashboard",
        description = "Sample dashboard for development",
        organization = "DocShow AI"
    )

    with ClientDatabaseManager() as session:
        manager = DashboardManager(session)
        existing_dashboard = manager.get_dashboard_by_name(dashboard.name, dashboard.organization)
        if not existing_dashboard:
            manager.create_dashboard(dashboard)
            logger.debug("Sample dashboard created.")
        else:
            logger.debug("Sample dashboard already exists.")
