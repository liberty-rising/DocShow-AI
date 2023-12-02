from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class Dashboard(Base):
    """
    Represents a dashboard which can contain multiple charts.

    Attributes:
    - id (int): Unique identifier for each dashboard.
    - name (str): Name of the dashboard.
    - description (str): A brief description of the dashboard.
    - organization (str): The organization associated with the dashboard.
    - charts (relationship): A list of 'Chart' objects associated with this dashboard.

    The 'charts' attribute represents a one-to-many relationship to the 'Chart' model,
    indicating that each dashboard can contain multiple charts.
    """

    __tablename__ = "dashboards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    organization = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())

    # Relationship to charts
    charts = relationship("Chart", back_populates="dashboard")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "organization": self.organization,
            "create_at": self.created_at,
            "updated_at": self.updated_at,
            "charts": [chart.to_dict() for chart in self.charts],
        }

    def __repr__(self):
        return f"<Dashboard(name='{self.name}', description='{self.description}')>"


class DashboardCreate(BaseModel):
    """
    Pydantic model representing the data required to create a new dashboard.

    Attributes:
        name (str): The desired name of the dashboard.
        description (str): The desired description for the dashboard.
        organization (str): The desired organization associated with the dashboard.
    """

    name: str
    description: str
    organization: str
