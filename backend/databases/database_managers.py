from settings import DB_SERVER_URL

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.engine = create_engine(f'{DB_SERVER_URL}{db_name}')

    def __enter__(self):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()
    
    def get_uri_str(self):
        return str(self.engine.url)

class AppDatabaseManager(DatabaseManager):
    def __init__(self):
        super().__init__('app_db')

class ClientDatabaseManager(DatabaseManager):
    def __init__(self):
        super().__init__('client_db')
class DataProfileManager:
    def __init__(self, session):
        self.session = session

    def get_dataprofile_by_name(self, name):
        """Retrieve a DataProfile by its name."""
        return self.session.query(DataProfile).filter(DataProfile.name == name).first()

    def create_dataprofile(self, data_profile):
        """Create a new DataProfile."""
        self.session.add(data_profile)
        self.session.commit()