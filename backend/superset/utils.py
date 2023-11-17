from models.app_models import User
from security import get_current_user
from session_config import session_manager
from superset.superset_manager import SupersetManager
from utils.utils import get_app_logger

from fastapi import Depends

logger = get_app_logger(__name__)

def get_superset_manager(user: User = Depends(get_current_user)):
    return SupersetManager(user.id, session_manager)