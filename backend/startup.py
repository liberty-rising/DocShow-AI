"""
Startup Module

This module contains functions that are executed during the startup of the application.
It checks the configuration settings and seeds the database when running in a development environment.

Usage:
    >>> from startup import run_startup_routines
    >>> run_startup_routines()
"""
from envs.dev.initialization.setup_dev_environment import create_admin_user, create_sample_dashboard, create_sample_organization, create_sample_dataprofile
from envs.dev.utils import seed_client_db
from settings import APP_ENV, JWT_SECRET_KEY
from utils.utils import get_app_logger


logger = get_app_logger(__name__)

def run_startup_routines():
    check_jwt_secret_key()

    if APP_ENV == 'development':
        create_sample_organization()
        create_admin_user()
        seed_client_db()
        create_sample_dashboard()
        create_sample_dataprofile()

def check_jwt_secret_key():
    if APP_ENV != 'development' and JWT_SECRET_KEY == 'mysecretkey':
        raise EnvironmentError("JWT_SECRET_KEY must be set in non-development environments")

