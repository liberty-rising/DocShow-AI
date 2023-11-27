"""
This module provides a OrganizationManager class that handles database operations related to the Organization model.
It uses SQLAlchemy for ORM operations and facilitates CRUD operations on user data.
"""
from sqlalchemy.orm import Session
from models.app_models import Organization

class OrganizationManager:
    """
    A class to manage CRUD operations related to the Organization model.
    
    Attributes:
        db_session (Session): An active database session for performing operations.
    """
    def __init__(self, session: Session):
        """
        Initializes the OrganizationManager with the given database session.
        
        Args:
            session (Session): The database session to be used for operations.
        """
        self.db_session = session

    def get_organization(self, org_id: int):
        """Get an organiation by id."""
        return self.db_session.query(Organization).filter(Organization.id == org_id).first()

    def get_organization_by_name(self, name: str):
        """
        Get an organization based on its name.
        
        Args:
            name (str): The name of the organization.
            
        Returns:
            Organization: The Organization object if found, else None.
        """
        return self.db_session.query(Organization).filter(Organization.name == name).first()
    
    def get_organizations(self):
        """Get a list of all of the organizations."""
        return self.db_session.query(Organization).all()

    def create_organization(self, organization: str):
        """
        Add a new organization to the database.
        
        Args:
            organization (Organization): The Organization object to be added.
            
        Returns:
            Organization: The created Organization object.
        """
        self.db_session.add(organization)
        self.db_session.commit()
        self.db_session.refresh(organization)
        return organization