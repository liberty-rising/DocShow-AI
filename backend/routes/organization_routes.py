from fastapi import APIRouter

from databases.database_managers import AppDatabaseManager
from databases.organization_manager import OrganizationManager

organization_router = APIRouter()

@organization_router.get("/organization/")
async def get_organization(org_id: int):
    with AppDatabaseManager() as session:
        org_manager = OrganizationManager(session)
        org = org_manager.get_organization(org_id)
    return org

@organization_router.get("/organizations/")
async def get_organizations():
    with AppDatabaseManager() as session:
        org_manager = OrganizationManager(session)
        orgs = org_manager.get_organizations()
    return orgs