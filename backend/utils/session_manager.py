import httpx

class SessionManager:
    """
    Manages and maintains individual HTTP sessions for users using the httpx Client.
    
    The class provides a centralized way to handle sessions for different users 
    to ensure that only one session is active for a user at any given time. 
    It allows easy retrieval, creation, and closing of sessions.

    Attributes:
        sessions (dict): A dictionary mapping user_ids to their respective httpx Client sessions.
    """
    def __init__(self):
        """
        Initializes a new instance of SessionManager with an empty sessions dictionary.
        """
        self.sessions = {}

    def get_session(self, user_id):
        """
        Retrieves the httpx Client session for the given user_id. 
        If a session does not exist for the user, it creates a new one.

        Args:
            user_id (int): The ID of the user for whom the session is to be retrieved or created.

        Returns:
            httpx.Client: The session associated with the given user_id.
        """
        if user_id not in self.sessions:
            self.sessions[user_id] = httpx.Client()
        return self.sessions[user_id]

    def close_session(self, user_id):
        """
        Closes and removes the httpx Client session for the given user_id if it exists.

        Args:
            user_id (int): The ID of the user for whom the session is to be closed.
        """
        if user_id in self.sessions:
            self.sessions[user_id].close()
            del self.sessions[user_id]
