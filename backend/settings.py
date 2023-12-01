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

ACCESS_TOKEN_EXPIRE_MINUTES = config('ACCESS_TOKEN_EXPIRE_MINUTES', default=30)
REFRESH_TOKEN_EXPIRE_DAYS = config('REFRESH_TOKEN_EXPIRE_DAYS', default=7)
JWT_SECRET_KEY = config('JWT_SECRET_KEY', default='mysecretkey')

DB_SERVER_URL = config('DB_SERVER_URL')

IS_HTTPS = config('IS_HTTPS').lower() == 'true'
OPENAI_API_KEY = config('OPENAI_API_KEY')