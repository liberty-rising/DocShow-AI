from database.database_manager import DatabaseManager
from database.organization_manager import OrganizationManager
from database.user_manager import UserManager
from models.organization import Organization
from models.user import User, UserRole
from security import get_password_hash
from utils.utils import get_app_logger

logger = get_app_logger(__name__)


def create_docshow_ai_organization():
    """Creates the DocShow AI organization if it doesn't already exist."""
    organization = Organization(name="DocShow AI")

    with DatabaseManager() as session:
        org_manager = OrganizationManager(session)
        existing_org = org_manager.get_organization_by_name(organization.name)
        if not existing_org:
            org_manager.create_organization(organization)
            logger.debug("DocShow AI organization created.")
        else:
            logger.debug("DocShow AI organization already exists.")


def create_admin_user():
    """Creates an admin user if it doesn't already exist."""
    admin_user = User(
        username="admin",
        hashed_password=get_password_hash("admin"),
        email="admin@docshow.ai",
        organization_id=1,
        role=UserRole.SYSTEM_ADMIN,
        requires_password_update=True,
        email_verified=True,
    )

    with DatabaseManager() as session:
        user_manager = UserManager(session)
        existing_user = user_manager.get_user_by_username(admin_user.username)
        if not existing_user:
            user_manager.create_user(admin_user)
            logger.debug("Admin user created.")
        else:
            logger.debug("Admin user already exists.")
