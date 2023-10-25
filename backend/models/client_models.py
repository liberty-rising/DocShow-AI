from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
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

# class LLM(Base):
#     """
#     Represents a Language Learning Model (LLM) in the database.

#     Attributes:
#         id (int): The unique identifier for each LLM.
#         name (str): The name or identifier of the LLM.
#         model_type (str): The type or architecture of the LLM.
#     """
#     __tablename__ = 'llm'
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     name = Column(String, unique=True)  # name or identifier of the LLM
#     model_type = Column(String)