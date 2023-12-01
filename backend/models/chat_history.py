from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from .base import Base

class ChatHistory(Base):
    """
    Represents a record of chat history between a user and an LLM.

    Attributes:
        id (int): The unique identifier for each chat message.
        chat_id (int): The id of the chat. Used to get the whole history of the chat.
        llm_type (int): The type of LLM involved in the chat (sql, chat, etc.).
        user_id (int): The identifier of the user involved in the chat.
        organization_id (int): The identifier of the organization involved in the chat
        message (str): The content of the message.
        is_user (bool): Indicates if the message is from the user (True) or LLM (False).
        timestamp (datetime): The timestamp when the message was created.
    """
    __tablename__ = 'chat_history'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    chat_id = Column(Integer, index=True)
    llm_type = Column(String, index=True)
    user_id = Column(Integer, index=True)
    organization_id = Column(Integer, index=True)
    message = Column(String)
    is_user = Column(Boolean)  # True if message is from user, False if from LLM
    timestamp = Column(DateTime(timezone=True), default=func.now())
