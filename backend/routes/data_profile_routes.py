from fastapi import APIRouter, Depends

from databases.database_manager import DatabaseManager
from databases.data_profile_manager import DataProfileManager
from models.user import User
from security import get_current_user

data_profile_router = APIRouter()


@data_profile_router.get("/data-profiles/")
async def get_data_profiles(current_user: User = Depends(get_current_user)):
    with DatabaseManager() as session:
        data_profile_manager = DataProfileManager(session)
        return data_profile_manager.get_all_data_profiles()
