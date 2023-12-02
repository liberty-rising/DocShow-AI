from settings import DB_SERVER_URL

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DatabaseManager:
    def __init__(self):
        self.engine = create_engine(f"{DB_SERVER_URL}db")

    def __enter__(self):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()

    def get_uri_str(self):
        return str(self.engine.url)
