from fastapi import APIRouter, HTTPException

from databases.database_manager import DatabaseManager
from databases.organization_manager import OrganizationManager
from models.organization import (
    Organization,
    OrganizationCreateRequest,
    OrganizationCreateResponse,
)

organization_router = APIRouter()


@organization_router.get("/organization/")
async def get_organization(org_id: int):
    with DatabaseManager() as session:
        org_manager = OrganizationManager(session)
        org = org_manager.get_organization(org_id)
    return org


@organization_router.get("/organizations/")
async def get_organizations():
    with DatabaseManager() as session:
        org_manager = OrganizationManager(session)
        orgs = org_manager.get_organizations()
    return orgs


@organization_router.post("/organization/")
async def save_organization(
    request: OrganizationCreateRequest,
) -> OrganizationCreateResponse:
    with DatabaseManager() as session:
        org_manager = OrganizationManager(session)
        if org_manager.get_organization_by_name(request.name):
            raise HTTPException(status_code=400, detail="Organization already exists")

        new_organization = Organization(name=request.name)
        created_organization = org_manager.create_organization(new_organization)
        response = OrganizationCreateResponse(created_organization.name)
        return response
