"""
This module provides a UserManager class that handles database operations related to the User model.
It uses SQLAlchemy for ORM operations and facilitates CRUD operations on user data.
"""
from typing import Optional

from sqlalchemy.orm import Session
from models.user import User, UserRole


class UserManager:
    """
    A class to manage CRUD operations related to the User model.

    Attributes:
        db_session (Session): An active database session for performing operations.
    """

    def __init__(self, session: Session):
        """
        Initializes the UserManager with the given database session.

        Args:
            session (Session): The database session to be used for operations.
        """
        self.db_session = session

    def get_user_by_email(self, email: str) -> User:
        """
        Get a user based on their email.

        Args:
            email (str): The email of the user.

        Returns:
            User: The User object if found, else None.
        """
        return self.db_session.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str) -> User:
        """
        Get a user based on their username.

        Args:
            username (str): The username of the user.

        Returns:
            User: The User object if found, else None.
        """
        return self.db_session.query(User).filter(User.username == username).first()

    def get_email(self, email: str):
        """
        Get a user based on their email.

        Args:
            email (str): The email of the user.

        Returns:
            User: The User object if found, else None.
        """
        return self.db_session.query(User).filter(User.email == email).first()

    def create_user(self, user: User) -> User:
        """
        Add a new user to the database.

        Args:
            user (User): The User object to be added.

        Returns:
            User: The created User object.
        """
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def get_users(self, skip: int = 0, limit: int = 10):
        """
        Retrieve a list of users from the database with pagination.

        Args:
            skip (int, optional): Number of entries to skip. Defaults to 0.
            limit (int, optional): Maximum number of entries to return. Defaults to 10.

        Returns:
            list[User]: List of User objects.
        """
        return self.db_session.query(User).offset(skip).limit(limit).all()

    def get_users_without_password(self, skip: int = 0, limit: int = 10):
        users = (
            self.db_session.query(User)
            .with_entities(
                User.id,
                User.role,
                User.email,
                User.organization_id,
                User.username,
                User.created_at,
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
        return users

    def update_user(
        self,
        user_id: int,
        email: Optional[str],
        organization_id: Optional[int],
        role: Optional[UserRole],
        refresh_token: Optional[str],
    ):
        """
        Update a user's details in the database.

        Args:
            user_id (int): The ID of the user to be updated.
            email (str, optional): The updated email. Defaults to None.
            organization_id (int, optional): The updated organization id. Defaults to None.
            role (UserRole, optional): The updated role. Defaults to None.
            refresh_token (str, optional): The updated refresh token. Defaults to None.

        Returns:
            User: The updated User object if found, else None.
        """
        db_user = self.db_session.query(User).filter(User.id == user_id).first()
        if db_user:
            if email:
                db_user.email = email
            if organization_id:
                db_user.organization_id = organization_id
            if role:
                db_user.role = role
            if refresh_token:
                db_user.refresh_token = refresh_token
            self.db_session.commit()
            self.db_session.refresh(db_user)
        return db_user

    def update_refresh_token(self, user_id: int, refresh_token: str):
        db_user = self.db_session.query(User).filter(User.id == user_id).first()
        if db_user:
            db_user.refresh_token = refresh_token
        self.db_session.commit()
        self.db_session.refresh(db_user)
        return db_user

    def update_user_by_username(
        self, username: str, organization_id: int, role: UserRole
    ) -> User:
        db_user = self.db_session.query(User).filter(User.username == username).first()
        if db_user:
            db_user.organization_id = organization_id
            db_user.role = role
            self.db_session.commit()
            self.db_session.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int):
        """
        Delete a user from the database.

        Args:
            user_id (int): The ID of the user to be deleted.

        Returns:
            User: The deleted User object if found, else None.
        """
        db_user = self.db_session.query(User).filter(User.id == user_id).first()
        if db_user:
            self.db_session.delete(db_user)
            self.db_session.commit()
            return db_user

    def update_user_password(self, username: str, new_hashed_password: str):
        """
        Update a user's password in the database.

        Args:
            old_password (str): The user's current password.
            new_password (str): The user's new password.

        Returns:
            User: The updated User object if found, else None.
        """
        db_user = self.db_session.query(User).filter(User.username == username).first()
        if db_user:
            db_user.hashed_password = new_hashed_password
            self.db_session.commit()
            self.db_session.refresh(db_user)
        return db_user

    def update_user_verification_token(self, username: str, verification_token: str):
        """
        Update a user's verification token in the database.

        Args:
            username (str): The user's username.
            verification_token (str): The user's verification token.

        Returns:
            User: The updated User object if found, else None.
        """
        db_user = self.db_session.query(User).filter(User.username == username).first()
        if db_user:
            db_user.verification_token = verification_token
            self.db_session.commit()
            self.db_session.refresh(db_user)
        return db_user

    def update_user_email_verified(self, username: str):
        """
        Update a user's email_verified in the database.

        Args:
            username (str): The user's username.

        Returns:
            User: The updated User object if found, else None.
        """
        db_user = self.db_session.query(User).filter(User.username == username).first()
        if db_user:
            db_user.email_verified = True
            self.db_session.commit()
            self.db_session.refresh(db_user)
        return db_user

    def update_user_requires_password_update(
        self, username: str, requires_password_update: bool
    ):
        """
        Update a user's requires_password_update in the database.

        Args:
            username (str): The user's username.

        Returns:
            User: The updated User object if found, else None.
        """
        db_user = self.db_session.query(User).filter(User.username == username).first()
        if db_user:
            db_user.requires_password_update = requires_password_update
            self.db_session.commit()
            self.db_session.refresh(db_user)
        return db_user

    def delete_user_by_username(self, username: str) -> User:
        """
        Delete a user based on their username.

        Args:
            username (str): The username of the user.

        Returns:
            User: The deleted User object if found, else None.
        """
        db_user = self.db_session.query(User).filter(User.username == username).first()
        if db_user:
            self.db_session.delete(db_user)
            self.db_session.commit()
        return db_user
