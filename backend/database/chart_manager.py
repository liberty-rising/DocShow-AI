from sqlalchemy.orm import Session
from models.chart import Chart


class ChartManager:
    """
    A class to manage operations related to the Chart model.

    Attributes:
        db_session (Session): An active database session for performing operations.
    """

    def __init__(self, db_session: Session):
        """
        Initializes the ChartManager with the given database session.

        Args:
            db_session (Session): The database session to be used for operations.
        """
        self.db_session = db_session

    def get_highest_order(self):
        highest_order_chart = (
            self.db_session.query(Chart).order_by(Chart.order.desc()).first()
        )
        if highest_order_chart:
            return highest_order_chart.order
        else:
            return -1

    def save_chart(self, chart: Chart):
        self.db_session.add(chart)
        self.db_session.commit()
        self.db_session.refresh(chart)
