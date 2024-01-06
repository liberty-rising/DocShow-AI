from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form

# from starlette.responses import JSONResponse
import tempfile
import os

from database.database_manager import DatabaseManager
from database.data_profile_manager import DataProfileManager
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
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name

    # Use the ImageConversionManager context manager to convert the PDF to JPG
    jpg_files = []
    with ImageConversionManager(temp_file_path, "/change-me/") as manager:
        jpg_files = manager.convert_to_jpg(temp_file_path)

    # Clean up the uploaded temp file
    os.unlink(temp_file_path)

    # Assuming you have a function to send the JPGs to the LLM and get a response
    # Send the JPG files to the LLM using the API
    # You need to define how you'll handle multiple JPGs - this is just a placeholder
    # if jpg_files:
    #     # Here you would typically prepare and send your request to the LLM API.
    #     # This will vary greatly depending on the LLM's API specifics.
    #     # For now, this is a placeholder for how you might make the request.
    #     # Replace with your actual API endpoint and key
    #     llm_api_endpoint = "https://api.example.com/llm"
    #     api_key = "your_api_key"
    #     response = requests.post(
    #         llm_api_endpoint,
    #         headers={"Authorization": f"Bearer {api_key}"},
    #         files={"file": open(jpg_files[0], "rb")},
    #     )

    #     # Handle the response
    #     if response.status_code == 200:
    #         llm_response = response.json()
    #     else:
    #         raise HTTPException(status_code=500, detail="LLM API request failed")
    # else:
    #     raise HTTPException(status_code=500, detail="Failed to convert file")

    # Clean up the created JPG files
    for jpg_file in jpg_files:
        os.unlink(jpg_file)

    # Return the LLM's response as JSON
    # return JSONResponse(content=llm_response)


# Now you would include this router in your FastAPI application instance.
# from fastapi import FastAPI
# app = FastAPI()
# app.include_router(data_profile_router)


# the response has to be a json

# file -- > convert to jpg --> |
# data-profile             --> | --> llm --> response
