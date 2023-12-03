from fastapi import APIRouter, HTTPException

from databases.database_manager import DatabaseManager
from databases.data_profile_manager import DataProfileManager
from models.data_profile import (
    DataProfile,
    DataProfileCreateRequest,
    DataProfileCreateResponse,
)

data_profile_router = APIRouter()


@data_profile_router.get("/data-profiles/")
async def get_data_profiles(organization_id: int):
    with DatabaseManager() as session:
        data_profile_manager = DataProfileManager(session)
        data_profile = data_profile_manager.get_all_data_profiles(organization_id)
    return data_profile


@data_profile_router.post("/data-profiles/")
async def save_data_profiles(
    request: DataProfileCreateRequest,
) -> DataProfileCreateResponse:
    with DatabaseManager() as session:
        data_profile_manager = DataProfileManager(session)
        if data_profile_manager.get_dataprofile_by_name(request.name):
            raise HTTPException(status_code=400, detail="Data Profile alredy exists")

        new_data_profile = DataProfile(name=request.name)
        created_data_profile = data_profile_manager.create_dataprofile(new_data_profile)
        response = DataProfileCreateResponse(created_data_profile.name)
        return response
