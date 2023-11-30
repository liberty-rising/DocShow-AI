from sqlalchemy.orm import joinedload, Session
from typing import List
from models.client.dashboard import Dashboard


class DashboardManager:
    """
    A class to manage operations related to the Dashboard model.
    
    Attributes:
        db_session (Session): An active database session for performing operations.
    """
    def __init__(self, db_session: Session):
        """
        Initializes the DashboardManager with the given database session.
        
        Args:
            db_session (Session): The database session to be used for operations.
        """
        self.db_session = db_session
    
    def get_dashboard(self, id: int):
        return self.db_session.query(Dashboard)\
            .options(joinedload(Dashboard.charts))\
            .filter(Dashboard.id == id)\
            .first()
    
    def get_dashboard_by_name(self, name: str, organization: str):
        return self.db_session.query(Dashboard).filter(
            Dashboard.name == name, Dashboard.organization == organization
        ).first()

    def get_dashboards(self) -> List[Dashboard]:
        """
        Retrieve all dashboards from the database.
        
        Returns:
            List[Dashboard]: List of Dashboard objects.
        """
        try:
            return self.db_session.query(Dashboard).all()
        except Exception as e:
            # Handle exception
            print(f"Database error: {str(e)}")
    
    def save_dashboard(self, dashboard: Dashboard):
        self.db_session.add(dashboard)
        self.db_session.commit()
        self.db_session.refresh(dashboard)