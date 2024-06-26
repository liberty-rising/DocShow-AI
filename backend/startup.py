"""
Startup Module

This module contains functions that are executed during the startup of the application.
It checks the configuration settings and seeds the database when running in a development environment.

Usage:
    >>> from startup import run_startup_routines
    >>> run_startup_routines()
"""
from envs.dev.initialization.setup_dev_environment import (
    create_admin_user as dev_create_admin_user,
)
from envs.dev.initialization.setup_dev_environment import (
    create_sample_dashboard,
    create_sample_dataprofile,
    create_sample_organization,
)
from envs.dev.utils import seed_db
from envs.prod.initialization.setup_prod_environment import (
    create_admin_user as prod_create_admin_user,
)
from envs.prod.initialization.setup_prod_environment import (
    create_docshow_ai_organization,
)
from settings import APP_ENV, JWT_SECRET_KEY
from utils.utils import get_app_logger

logger = get_app_logger(__name__)


def run_startup_routines():
    check_jwt_secret_key()

    if APP_ENV == "dev":
        create_sample_organization()
        dev_create_admin_user()
        seed_db()
        create_sample_dashboard()
        create_sample_dataprofile()

    if APP_ENV == "prod":
        create_docshow_ai_organization()
        prod_create_admin_user()


def check_jwt_secret_key():
    if APP_ENV != "dev" and JWT_SECRET_KEY == "mysecretkey":
        raise EnvironmentError(
            "JWT_SECRET_KEY must be set in non-development environments"
        )
