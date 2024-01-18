from settings import (
    APP_ENV,
    DATABASE_POOL_MAX_OVERFLOW,
    DATABASE_POOL_SIZE,
    DATABASE_URL,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool


class DatabaseManager:
    def __init__(self):
        if APP_ENV == "prod":
            self.engine = create_engine(
                DATABASE_URL,
                poolclass=QueuePool,
                pool_size=DATABASE_POOL_SIZE,
                max_overflow=DATABASE_POOL_MAX_OVERFLOW,
            )
        else:
            self.engine = create_engine(DATABASE_URL)

    def __enter__(self):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()

    def get_uri_str(self):
        return str(self.engine.url)
