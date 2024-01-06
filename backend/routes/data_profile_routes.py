from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form

import tempfile

from database.database_manager import DatabaseManager
from database.data_profile_manager import DataProfileManager
from llms.gpt import GPTLLM
from models.data_profile import (
    DataProfile,
    DataProfileCreateRequest,
    DataProfileCreateResponse,
)
from models.user import User
from security import get_current_user
from utils.image_conversion_manager import ImageConversionManager

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
            raise HTTPException(status_code=400, detail="Data Profile already exists")

        new_data_profile = DataProfile(
            name=request.name,
            description=request.description,
        )
        created_data_profile = data_profile_manager.create_dataprofile(new_data_profile)

        # Make sure to pass the fields as keyword arguments
        response = DataProfileCreateResponse(
            name=created_data_profile.name,
            description=created_data_profile.description,
        )
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


@data_profile_router.post("/data-profiles/preview/")
async def preview_data_profile(
    file: UploadFile = File(...),
    instructions: str = Form(...),
    current_user: User = Depends(get_current_user),
):
    suffix = file.filename.split(".")[-1]
    # Save the uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=True, suffix=suffix) as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name

        # Use the ImageConversionManager context manager to convert the PDF to JPG
        with ImageConversionManager(temp_file_path, "/tmp/") as manager:
            jpg_file = manager.convert_to_jpg(temp_file_path)
            gpt = GPTLLM()
            data = gpt.extract_data_from_jpg(instructions, jpg_file)
        return data


# the response has to be a json

# file -- > convert to jpg --> |
# data-profile             --> | --> llm --> response
