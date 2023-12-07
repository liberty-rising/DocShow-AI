from fastapi import APIRouter, HTTPException, Depends

from databases.database_manager import DatabaseManager
from databases.data_profile_manager import DataProfileManager
from models.data_profile import (
    DataProfile,
    DataProfileCreateRequest,
    DataProfileCreateResponse,
)
from models.user import User
from security import get_current_user


data_profile_router = APIRouter()


@data_profile_router.get("/data-profiles/")
async def get_data_profiles(current_user: User = Depends(get_current_user)):
    with DatabaseManager() as session:
        data_profile_manager = DataProfileManager(session)
        data_profiles = data_profile_manager.get_all_data_profiles()
        return data_profiles


@data_profile_router.post("/data-profile/")
async def save_data_profiles(
    request: DataProfileCreateRequest, current_user: User = Depends(get_current_user)
) -> DataProfileCreateResponse:
    with DatabaseManager() as session:
        data_profile_manager = DataProfileManager(session)
        if data_profile_manager.get_dataprofile_by_name(request.name):
            raise HTTPException(status_code=400, detail="Data Profile alredy exists")

        new_data_profile = DataProfile(name=request.name)
        created_data_profile = data_profile_manager.create_dataprofile(new_data_profile)
        response = DataProfileCreateResponse(created_data_profile.name)
        return response


@data_profile_router.get("/data-profiles/{data_profile_id}")
async def get_data_profile(
    data_profile_id: int, current_user: User = Depends(get_current_user)
):
    with DatabaseManager() as session:
        data_profile_manager = DataProfileManager(session)
        data_profile = data_profile_manager.get_dataprofile_by_id(data_profile_id)
        if data_profile is None:
            raise HTTPException(status_code=404, detail="Data Profile not found")
        return data_profile
