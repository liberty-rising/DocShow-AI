from models.data_profile import DataProfile


class DataProfileManager:
    def __init__(self, session):
        self.session = session

    def get_dataprofile_by_name_and_org(self, name, org_id) -> DataProfile:
        """Retrieve a DataProfile by its name."""
        return (
            self.session.query(DataProfile)
            .filter(DataProfile.name == name)
            .filter(DataProfile.organization_id == org_id)
            .first()
        )

    def get_all_data_profiles(self):
        """Retrieve all DataProfiles."""
        return self.session.query(DataProfile).all()

    def get_all_data_profile_names_by_org_id(self, org_id):
        """Retrieve all DataProfiles."""
        result = (
            self.session.query(DataProfile.name)
            .filter(DataProfile.organization_id == org_id)
            .all()
        )
        data_profile_names = [name for (name,) in result]
        return data_profile_names

    def create_dataprofile(self, data_profile: DataProfile):
        """Create a new DataProfile."""
        self.session.add(data_profile)
        self.session.commit()
        return data_profile

    def get_dataprofile_by_id(self, data_profile_id: int):
        """Retrieve a DataProfile by its ID."""
        return (
            self.session.query(DataProfile)
            .filter(DataProfile.id == data_profile_id)
            .first()
        )

    def delete_dataprofile(self, data_profile_id: int):
        """Delete a DataProfile."""
        self.session.query(DataProfile).filter(
            DataProfile.id == data_profile_id
        ).delete()
        self.session.commit()
        return True
