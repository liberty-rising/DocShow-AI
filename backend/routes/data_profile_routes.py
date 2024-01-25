import os
import tempfile
from typing import List

from database.data_profile_manager import DataProfileManager
from database.database_manager import DatabaseManager
from database.organization_manager import OrganizationManager
from database.table_manager import TableManager
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from llms.gpt import GPTLLM
from models.data_profile import (
    DataProfile,
    DataProfileCreateRequest,
    DataProfileCreateResponse,
)
from models.user import User
from object_storage.digitalocean_space_manager import DigitalOceanSpaceManager
from security import get_current_user
from utils.image_conversion_manager import ImageConversionManager

data_profile_router = APIRouter()


@data_profile_router.get("/data-profiles/")
async def get_data_profiles(current_user: User = Depends(get_current_user)):
    with DatabaseManager() as session:
        data_profile_manager = DataProfileManager(session)
        data_profiles = data_profile_manager.get_all_data_profiles()
        return data_profiles


@data_profile_router.get("/data-profiles/org/")
async def get_data_profiles_by_org_id(current_user: User = Depends(get_current_user)):
    with DatabaseManager() as session:
        data_profile_manager = DataProfileManager(session)
        data_profile_names = data_profile_manager.get_all_data_profile_names_by_org_id(
            current_user.organization_id
        )
    return data_profile_names


@data_profile_router.post("/data-profile/")
async def save_data_profile(
    request: DataProfileCreateRequest, current_user: User = Depends(get_current_user)
) -> DataProfileCreateResponse:
    """Save a new data profile to the database"""
    with DatabaseManager() as session:
        data_profile_manager = DataProfileManager(session)
        if data_profile_manager.get_dataprofile_by_name_and_org(
            request.name, current_user.organization_id
        ):
            raise HTTPException(status_code=400, detail="Data Profile already exists")

        new_data_profile = DataProfile(
            name=request.name,
            extract_instructions=request.extract_instructions,
            organization_id=current_user.organization_id,
        )
        created_data_profile = data_profile_manager.create_dataprofile(new_data_profile)

        # Make sure to pass the fields as keyword arguments
        response = DataProfileCreateResponse(
            name=created_data_profile.name,
            extract_instructions=created_data_profile.extract_instructions,
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
    files: List[UploadFile] = File(...),
    extract_instructions: str = Form(...),
    current_user: User = Depends(get_current_user),
):
    preview_data_profile = DataProfile(
        name="preview", extract_instructions=extract_instructions
    )

    temp_file_paths = []
    for file in files:
        if file.filename:
            suffix = file.filename.split(".")[-1]

        # Save the uploaded file temporarily
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix="." + suffix)
        temp_file.write(await file.read())
        temp_file.close()
        temp_file_paths.append(temp_file.name)

    # Get the organization name
    with DatabaseManager() as session:
        org_manager = OrganizationManager(session)
        organization_name = org_manager.get_organization(
            current_user.organization_id
        ).name

    # Use the ImageConversionManager context manager to convert the PDF to JPG
    with ImageConversionManager(temp_file_paths) as manager:
        jpg_file_paths = manager.convert_to_jpgs()

        # Upload the JPG file to DigitalOcean Spaces, automatically deleting it when done
        with DigitalOceanSpaceManager(
            organization_name=organization_name, file_paths=jpg_file_paths
        ) as space_manager:
            space_manager.upload_files_by_paths()
            jpg_presigned_urls = space_manager.create_presigned_urls()
            gpt = GPTLLM(chat_id=1, user=current_user)
            extracted_data = await gpt.extract_data_from_jpgs(
                preview_data_profile, jpg_presigned_urls
            )

    # Delete the temporary files
    for path in temp_file_paths:
        os.remove(path)

    return extracted_data


@data_profile_router.post("/data-profiles/{data_profile_name}/preview/")
async def preview_data_profile_upload(
    data_profile_name: str,
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
):
    temp_file_paths = []
    for file in files:
        if file.filename:
            suffix = file.filename.split(".")[-1]

        # Save the uploaded file temporarily
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix="." + suffix)
        temp_file.write(await file.read())
        temp_file.close()
        temp_file_paths.append(temp_file.name)

    # Get the organization name
    with DatabaseManager() as session:
        org_manager = OrganizationManager(session)
        organization_name = org_manager.get_organization(
            current_user.organization_id
        ).name

        data_profile_manager = DataProfileManager(session)
        data_profile = data_profile_manager.get_dataprofile_by_name_and_org(
            data_profile_name, current_user.organization_id
        )

    # Use the ImageConversionManager context manager to convert the PDF to JPG
    with ImageConversionManager(temp_file_paths) as manager:
        jpg_file_paths = manager.convert_to_jpgs()

        # Upload the JPG file to DigitalOcean Spaces, automatically deleting it when done
        with DigitalOceanSpaceManager(
            organization_name=organization_name, file_paths=jpg_file_paths
        ) as space_manager:
            space_manager.upload_files_by_paths()
            jpg_presigned_urls = space_manager.create_presigned_urls()
            gpt = GPTLLM(chat_id=1, user=current_user)
            extracted_data = await gpt.extract_data_from_jpgs(
                data_profile, jpg_presigned_urls
            )

    # Delete the temporary files
    for path in temp_file_paths:
        os.remove(path)

    return extracted_data


@data_profile_router.post("/data-profiles/{data_profile_name}/extracted-data/")
async def save_extracted_data(
    data_profile_name: str,
    extracted_data: dict,
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
):
    # Get the organization name
    with DatabaseManager() as session:
        org_manager = OrganizationManager(session)
        organization_name = org_manager.get_organization(
            current_user.organization_id
        ).name

        data_profile_manager = DataProfileManager(session)
        data_profile: DataProfile = (
            data_profile_manager.get_dataprofile_by_name_and_org(
                data_profile_name, current_user.organization_id
            )
        )

        table_manager = TableManager(session)
        print(data_profile, table_manager)  # TODO: To be further implemented

    # Upload the JPG file to DigitalOcean Spaces, automatically deleting it when done
    with DigitalOceanSpaceManager(
        organization_name=organization_name, files=files
    ) as space_manager:
        space_manager.upload_files()

    return {"message": "Extracted data saved successfully"}
