from models.client.data_profile import DataProfile

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