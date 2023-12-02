from sqlalchemy.orm import Session
from models.chat_history import ChatHistory  # Replace with your actual import

import json


class ChatHistoryManager:
    """
    Class for managing chat history between users and LLMs.

    Attributes:
        db (Session): SQLAlchemy Session object for database interactions.
    """

    def __init__(self, session: Session):
        """
        Initialize the ChatHistoryManager with a database session.

        Args:
            db (Session): SQLAlchemy Session object.
        """
        self.session = session

    def get_history(self, chat_id: int):
        """
        Fetch chat history messages for a specific chat id.
        """
        chat_history = (
            self.session.query(ChatHistory)
            .filter(ChatHistory.id == chat_id)
            .order_by(ChatHistory.timestamp.asc())
            .all()
        )

        # Deserialize the JSON strings to Python dictionaries and extract messages
        messages = [json.loads(record.message) for record in chat_history]

        return messages

    def get_new_chat_id(self) -> int:
        """
        Get a new chat id. Used for storing a new chat.
        """
        latest_chat = (
            self.session.query(ChatHistory).order_by(ChatHistory.chat_id.desc()).first()
        )

        if not latest_chat:  # If there are no chats in database
            return 0

        return latest_chat.chat_id + 1

    def get_llm_chat_history_for_user(self, user_id: int, llm_type: str):
        """
        Fetch the chat history messages for a specific user and LLM.

        Args:
            user_id (int): The identifier of the user.
            llm_type (str): The type of the LLM.

        Returns:
            List[ChatHistory]: List of ChatHistory objects sorted by timestamp.
        """
        chat_history = (
            self.session.query(ChatHistory)
            .filter(ChatHistory.user_id == user_id, ChatHistory.llm_type == llm_type)
            .order_by(ChatHistory.timestamp.asc())
            .all()
        )

        # Deserialize the JSON strings to Python dictionaries and extract messages
        messages = [json.loads(record.message) for record in chat_history]

        return messages

    def save_message(self, chat_id, user_id, llm_type, message, is_user):
        new_record = ChatHistory(
            chat_id=chat_id,
            user_id=user_id,
            llm_type=llm_type,
            message=message,
            is_user=is_user,
        )
        self.session.add(new_record)
        self.session.commit()

    def delete_chat_history(self, user_id):
        """
        Delete the chat history for a specific user.

        Args:
            user_id (int): The identifier of the user.
        """
        # Query to find all chat history for the given user_id
        chat_history_query = self.session.query(ChatHistory).filter(
            ChatHistory.user_id == user_id
        )

        # Delete the records
        chat_history_query.delete(synchronize_session=False)

        # Commit the transaction
        self.session.commit()
