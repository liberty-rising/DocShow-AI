from pydantic import BaseModel
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

class TableMetadata(Base):
    """
    Represents metadata for a table in the database.

    Attributes:
        table_name (str): The name of the table, used as the primary key.
        create_statement (str): The SQL statement used to create the table.
        description (str): A description of the table.
    """
    __tablename__ = 'table_metadata'
    table_name = Column(String, primary_key=True, index=True)
    create_statement = Column(String)
    description = Column(String)

    def to_dict(self):
        return {
            "table_name": self.table_name,
            "create_statement": self.create_statement,
            "description": self.description
        }

class ChatHistory(Base):
    """
    Represents a record of chat history between a user and an LLM.

    Attributes:
        id (int): The unique identifier for each chat message.
        llm_type (int): The type of LLM involved in the chat (sql, chat, etc.).
        user_id (int): The identifier of the user involved in the chat.
        message (str): The content of the message.
        is_user (bool): Indicates if the message is from the user (True) or LLM (False).
        timestamp (datetime): The timestamp when the message was created.
    """
    __tablename__ = 'chat_history'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    llm_type = Column(String, index=True)
    user_id = Column(Integer, index=True)  # Assuming user_id is a string
    message = Column(String)
    is_user = Column(Boolean)  # True if message is from user, False if from LLM
    timestamp = Column(DateTime(timezone=True), default=func.now())

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
            "charts": [chart.to_dict() for chart in self.charts]
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