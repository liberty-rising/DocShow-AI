from database.database_manager import DatabaseManager
from database.user_manager import UserManager
from models.user import User
from security import get_password_hash
from utils.utils import get_app_logger

logger = get_app_logger(__name__)


def create_admin_user():
    """Creates an admin user if it doesn't already exist."""
    admin_user = User(
        username="admin",
        hashed_password=get_password_hash("admin"),
        email="admin@docshow.ai",
        organization_id=1,
        role="admin",
        requires_password_update=True,
    )

    with DatabaseManager() as session:
        user_manager = UserManager(session)
        existing_user = user_manager.get_user_by_username(admin_user.username)
        if not existing_user:
            user_manager.create_user(admin_user)
            logger.debug("Admin user created.")
        else:
            logger.debug("Admin user already exists.")
