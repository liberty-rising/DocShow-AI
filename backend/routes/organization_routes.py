from database.database_manager import DatabaseManager
from database.organization_manager import OrganizationManager
from fastapi import APIRouter, Depends, HTTPException
from models.organization import (
    Organization,
    OrganizationCreateRequest,
    OrganizationCreateResponse,
)
from models.user import User
from security import get_current_admin_user, get_current_user

organization_router = APIRouter()


@organization_router.get("/organization/")
async def get_organization(org_id: int, current_user: User = Depends(get_current_user)):
    with DatabaseManager() as session:
        org_manager = OrganizationManager(session)
        org = org_manager.get_organization(org_id)
    return org


@organization_router.get("/organizations/")
async def get_organizations(current_admin: User = Depends(get_current_admin_user)):
    with DatabaseManager() as session:
        org_manager = OrganizationManager(session)
        orgs = org_manager.get_organizations()
    return orgs


@organization_router.post("/organization/", response_model=OrganizationCreateResponse)
async def save_organization(
    org: OrganizationCreateRequest, current_user: User = Depends(get_current_user)
):
    with DatabaseManager() as session:
        org_manager = OrganizationManager(session)
        if org_manager.get_organization_by_name(org.name):
            raise HTTPException(status_code=400, detail="Organization already exists")

        new_organization = Organization(name=org.name)
        created_organization = org_manager.create_organization(new_organization)
        response = OrganizationCreateResponse(name=created_organization.name)
        return response


@organization_router.delete("/organization/{org_id}")
async def delete_organization(
    org_id: int, current_admin: User = Depends(get_current_admin_user)
):
    with DatabaseManager() as session:
        org_manager = OrganizationManager(session)
        org_manager.delete_organization(org_id)
    return {"detail": "Organization deleted successfully"}
