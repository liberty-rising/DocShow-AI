"""
Settings Module

This module loads configuration values from environment variables using the
python-decouple library. Environment variables are defined in a .env file
located at the project's root.

Example:
    >>> from settings import DEBUG, JWT_SECRET_KEY

"""
from decouple import config

APP_ENV = config("APP_ENV")
APP_HOST = config("APP_HOST")

ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)
REFRESH_TOKEN_EXPIRE_DAYS = config("REFRESH_TOKEN_EXPIRE_DAYS", default=7)
JWT_SECRET_KEY = config("JWT_SECRET_KEY")

DB_URL = config("DB_URL")

OPENAI_API_KEY = config("OPENAI_API_KEY")

PASSWORD_RESET_EXPIRE_MINUTES = int(config("PASSWORD_RESET_EXPIRE_MINUTES", default=15))

SENDGRID_API_KEY = config("SENDGRID_API_KEY")
