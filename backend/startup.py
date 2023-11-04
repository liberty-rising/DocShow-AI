"""
Startup Module

This module contains functions that are executed during the startup of the application.
It checks the configuration settings and seeds the database when running in a development environment.

Usage:
    >>> from startup import run_startup_routines
    >>> run_startup_routines()
"""
from databases.database_managers import AppDatabaseManager
from databases.user_manager import UserManager
from envs.dev.utils import seed_client_db
from models.app_models import User
from security import get_password_hash
from settings import APP_ENV, JWT_SECRET_KEY
from superset.utils import seed_superset
from utils.utils import get_app_logger


logger = get_app_logger(__name__)

def run_startup_routines():
    check_jwt_secret_key()

    if APP_ENV == 'development':
        create_admin_user()
        seed_client_db()
        seed_superset()

def check_jwt_secret_key():
    if APP_ENV != 'development' and JWT_SECRET_KEY == 'mysecretkey':
        raise EnvironmentError("JWT_SECRET_KEY must be set in non-development environments")

def create_admin_user():
    """Creates an admin user if it doesn't already exist."""
    admin_user = User(
        username = 'admin',
        hashed_password = get_password_hash('admin'),
        email = 'admin@docshow.ai',
        organization = 'docshowai',
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