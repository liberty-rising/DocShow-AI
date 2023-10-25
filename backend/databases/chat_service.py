from sqlalchemy.orm import Session
from models.client_models import ChatHistory  # Replace with your actual import

import json

class ChatHistoryService:
    """
    Service class for managing chat history between users and LLMs.

    Attributes:
        db (Session): SQLAlchemy Session object for database interactions.
    """
    def __init__(self, db: Session):
        """
        Initialize the ChatHistoryService with a database session.

        Args:
            db (Session): SQLAlchemy Session object.
        """
        self.db = db

    def get_llm_chat_history_for_user(self, user_id: int, llm_type: str):
        """
        Fetch the chat history for a specific user and LLM.

        Args:
            user_id (int): The identifier of the user.
            llm_type (str): The type of the LLM.

        Returns:
            List[ChatHistory]: List of ChatHistory objects sorted by timestamp.
        """
        chat_history = self.db.query(ChatHistory).filter(
            ChatHistory.user_id == user_id,
            ChatHistory.llm_type == llm_type
        ).order_by(ChatHistory.timestamp.asc()).all()

        # Deserialize the JSON strings to Python dictionaries
        for record in chat_history:
            record.message = json.loads(record.message)

        return chat_history
    
    def save_message(self, user_id, llm_type, message, is_user):
        new_record = ChatHistory(
            user_id=user_id,
            llm_type=llm_type,
            message=message,
            is_user=is_user
        )
        self.db.add(new_record)
        self.db.commit()