# databases/user_manager.py
from sqlalchemy.orm import Session
from models.app_models import User
from security import get_password_hash

class UserManager:
    def __init__(self, session: Session):
        self.db_session = session

    def get_user(self, username: str):
        return self.db_session.query(User).filter(User.username == username).first()

    def create_user(self, username: str, email: str, password: str, organization: str = None, role: str = None):
        hashed_password = get_password_hash(password)
        db_user = User(username=username, email=email, hashed_password=hashed_password, organization=organization, role=role)
        self.db_session.add(db_user)
        self.db_session.commit()
        self.db_session.refresh(db_user)
        return db_user

    def get_users(self, skip: int = 0, limit: int = 10):
        return self.db_session.query(User).offset(skip).limit(limit).all()

    def update_user(self, user_id: int, email: str = None, organization: str = None, role: str = None):
        db_user = self.db_session.query(User).filter(User.id == user_id).first()
        if db_user:
            if email:
                db_user.email = email
            if organization:
                db_user.organization = organization
            if role:
                db_user.role = role
            self.db_session.commit()
            self.db_session.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int):
        db_user = self.db_session.query(User).filter(User.id == user_id).first()
        if db_user:
            self.db_session.delete(db_user)
            self.db_session.commit()
            return db_user
