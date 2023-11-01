"""
Settings Module

This module loads configuration values from environment variables using the
python-decouple library. Environment variables are defined in a .env file
located at the project's root.

Example:
    >>> from settings import DEBUG, JWT_SECRET_KEY

"""
from decouple import config

APP_ENV = config('APP_ENV')
APP_DB_URL = config('APP_DB_URL')
ACCESS_TOKEN_EXPIRE_MINUTES = config('ACCESS_TOKEN_EXPIRE_MINUTES', default=30)
CLIENT_DB_URL = config('CLIENT_DB_URL')
DB_SERVER_URL = config('DB_SERVER_URL')
JWT_SECRET_KEY = config('JWT_SECRET_KEY', default='mysecretkey')
OPENAI_API_KEY = config('OPENAI_API_KEY')