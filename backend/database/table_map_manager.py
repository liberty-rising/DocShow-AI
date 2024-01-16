from typing import List

from fastapi import HTTPException
from models.table_map import TableMap
from sqlalchemy.orm import Session


class TableMapManager:
    """
    A class to manage CRUD operations related to the TableMap model.

    Attributes:
        db_session (Session): An active database session for performing operations.
    """

    def __init__(self, session: Session):
        """
        Initializes the TableMap with the given database session.

        Args:
            db_session (Session): The database session to be used for operations.
        """
        self.db_session = session

    def create_table_map(self, table_map: TableMap):
        """
        Add a new table map to the database.

        Args:
            table_map (TableMap): The TableMap object to be added.

        Returns:
            TableMap: The created TableMap object.
        """
        try:
            if self.db_session:
                self.db_session.add(table_map)
                self.db_session.commit()
                return table_map
        except Exception as e:
            self.db_session.rollback() if self.db_session else None
            print(f"An error occurred: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    def get_org_tables(self, org_id: int) -> List:
        """Returns a list of names of all of the tables associated with an organization."""
        try:
            if self.db_session:
                table_names = (
                    self.db_session.query(TableMap.table_name)
                    .filter(TableMap.organization_id == org_id)
                    .all()
                )
                return [
                    name[0] for name in table_names
                ]  # Extracting table_name from each tuple
            return []
        except Exception as e:
            self.db_session.rollback() if self.db_session else None
            print(f"An error occurred: {e}")
            raise HTTPException(status_code=400, detail=str(e))
