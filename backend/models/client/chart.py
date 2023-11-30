from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from .base import Base

class Chart(Base):
    """
    Represents a chart in a dashboard.

    Attributes:
    - id (int): Unique identifier for each chart.
    - dashboard_id (int): Foreign key linking the chart to its dashboard.
    - order (int): Integer indicating the chart's position on the dashboard.
    - config = (JSONB): The configuration of the chart. Specifies attributes such as chart type, data source structure, query, styling, etc.
    - dashboard (relationship): Relationship back to the Dashboard model.
    """
    __tablename__ = 'charts'

    id = Column(Integer, primary_key=True)
    dashboard_id = Column(Integer, ForeignKey('dashboards.id'))
    order = Column(Integer)
    config = Column(JSONB)  # Note: JSONB is specific to PostgreSQL

    # Relationship to dashboard
    dashboard = relationship("Dashboard", back_populates="charts")

    def to_dict(self):
        return {
            "id": self.id,
            "dashboard_id": self.dashboard_id,
            "order": self.order,
            "config": self.config
        }

    def __repr__(self):
        """Provide a readable representation of a Chart object."""
        return f"<Chart(id={self.id}, dashboard_id={self.dashboard_id}, order={self.order}, config={self.config})>"

class ChartCreate(BaseModel):
    """
    Pydantic model representing the data required to create a new chart.
    
    Attributes:
        dashboard_id (int): The id of the associated dashboard.
        config (dict): The configuration settings for the chart.
    """
    dashboard_id: int
    config: dict