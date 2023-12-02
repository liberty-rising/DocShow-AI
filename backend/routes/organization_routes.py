from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from databases.database_manager import DatabaseManager
from databases.organization_manager import OrganizationManager
from models.organization import Organization  

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

class OrganizationCreateRequest(BaseModel):
    name: str

@organization_router.post("/organizations/add")
async def add_organization(request: OrganizationCreateRequest):
    with DatabaseManager() as session:
        org_manager = OrganizationManager(session)
        if org_manager.get_organization_by_name(request.name):
            raise HTTPException(status_code=400, detail="Organization already exists")
        new_organization = Organization(name=request.name)
        created_organization = org_manager.create_organization(new_organization)
        return {"message": "Organization created successfully", "organization": created_organization.name}