"""
session_config.py

This module is responsible for managing sessions for the application.

It centralizes the creation and management of the session manager to avoid circular imports and allow easy access across different modules.

Attributes:
    session_manager (SessionManager): A SessionManager instance that manages Superset sessions for different user_ids.
"""
from utils.session_manager import SessionManager

session_manager = SessionManager()
