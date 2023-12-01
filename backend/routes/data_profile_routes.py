from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from databases.database_managers import ClientDatabaseManager
from databases.data_profile_manager import DataProfileManager

data_profile_router = APIRouter()

@data_profile_router.get("/data-profiles/")
async def get_data_profiles():
    with ClientDatabaseManager() as session:
        data_profile_manager = DataProfileManager(session)
        return data_profile_manager.get_all_data_profiles()