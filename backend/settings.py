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

AZURE_CLIENT_ID = config("AZURE_CLIENT_ID")
AZURE_TENANT_ID = config("AZURE_TENANT_ID")
AZURE_APP_VALUE = config("AZURE_APP_VALUE")
AZURE_APP_SECRET = config("AZURE_APP_SECRET")

ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)
REFRESH_TOKEN_EXPIRE_DAYS = config("REFRESH_TOKEN_EXPIRE_DAYS", default=1)
REMEMBER_ME_ACCESS_TOKEN_EXPIRE_MINUTES = config(
    "REMEMBER_ME_ACCESS_TOKEN_EXPIRE_MINUTES", default=30
)
REMEMBER_ME_REFRESH_TOKEN_EXPIRE_DAYS = config(
    "REMEMBER_ME_REFRESH_TOKEN_EXPIRE_DAYS", default=7
)
JWT_SECRET_KEY = config("JWT_SECRET_KEY")

DATABASE_URL = config(
    "DATABASE_URL", default="postgresql://admin:admin@postgres_db:5432/db"
)
DATABASE_POOL_URL = config("DATABASE_POOL_URL", default=None)
DATABASE_POOL_SIZE = int(config("DATABASE_POOL_SIZE", default=10))
DATABASE_POOL_MAX_OVERFLOW = int(config("DATABASE_POOL_MAX_OVERFLOW", default=3))
DATABASE_LANGCHAIN_POOL_SIZE = int(config("DATABASE_LANGCHAIN_POOL_SIZE", default=5))
DATABASE_LANGCHAIN_POOL_MAX_OVERFLOW = int(
    config("DATABASE_LANGCHAIN_POOL_MAX_OVERFLOW", default=2)
)

EMAIL_VERIFICATION_EXPIRE_MINUTES = int(
    config("EMAIL_VERIFICATION_EXPIRE_MINUTES", default=15)
)

OPENAI_API_KEY = config("OPENAI_API_KEY")

PASSWORD_RESET_EXPIRE_MINUTES = int(config("PASSWORD_RESET_EXPIRE_MINUTES", default=15))

SENDGRID_API_KEY = config("SENDGRID_API_KEY")

SPACES_ACCESS_KEY = config("SPACES_ACCESS_KEY")
SPACES_BUCKET_NAME = config("SPACES_BUCKET_NAME")
SPACES_ENDPOINT_URL = config("SPACES_ENDPOINT_URL")
SPACES_REGION_NAME = config("SPACES_REGION_NAME")
SPACES_SECRET_ACCESS_KEY = config("SPACES_SECRET_ACCESS_KEY")
