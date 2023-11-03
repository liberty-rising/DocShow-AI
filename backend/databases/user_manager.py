# databases/user_manager.py
from sqlalchemy.orm import Session
from models.app_models import User

class UserManager:
    def __init__(self, session: Session):
        self.db_session = session
    
    @staticmethod
    def get_current_user_id():
        # TODO: Implement logic to get the current user id
        return 1

    def get_user(self, username: str):
        return self.db_session.query(User).filter(User.username == username).first()
    
    def get_email(self, email: str):
        return self.db_session.query(User).filter(User.email == email).first()

    def create_user(self, user: User):
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

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
