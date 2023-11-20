from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
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
    - type (str): Type of the chart (e.g., bar, line, pie).
    - data_source (str): Information about the data source for the chart.
    - order (int): Integer indicating the chart's position on the dashboard.
    - dashboard (relationship): Relationship back to the Dashboard model.
    """
    __tablename__ = 'charts'

    id = Column(Integer, primary_key=True)
    dashboard_id = Column(Integer, ForeignKey('dashboards.id'))
    type = Column(String)
    data_source = Column(String)
    order = Column(Integer)

    # Relationship to dashboard
    dashboard = relationship("Dashboard", back_populates="charts")

    def __repr__(self):
        """Provide a readable representation of a Chart object."""
        return f"<Chart(type='{self.type}', data_source='{self.data_source}', order={self.order})>"