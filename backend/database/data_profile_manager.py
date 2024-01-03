from models.data_profile import DataProfile, DataProfileCreateRequest


class DataProfileManager:
    def __init__(self, session):
        self.session = session

    def get_dataprofile_by_name(self, name):
        """Retrieve a DataProfile by its name."""
        return self.session.query(DataProfile).filter(DataProfile.name == name).first()

    def get_all_data_profiles(self):
        """Retrieve all DataProfiles."""
        return self.session.query(DataProfile).all()

    def create_dataprofile(self, data_profile_data: DataProfileCreateRequest):
        """Create a new DataProfile."""
        new_data_profile = DataProfile(
            name=data_profile_data.name,
            file_type=data_profile_data.file_type,
            organization_id=data_profile_data.organization_id,
            description=data_profile_data.description,
        )
        self.session.add(new_data_profile)
        self.session.commit()
        return new_data_profile

    def get_dataprofile_by_id(self, data_profile_id: int):
        """Retrieve a DataProfile by its ID."""
        return (
            self.session.query(DataProfile)
            .filter(DataProfile.id == data_profile_id)
            .first()
        )