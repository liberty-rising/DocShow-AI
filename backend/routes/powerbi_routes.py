from fastapi import APIRouter
from models.powerbi import GenerateEmbededTokenRequest
from utils.azure.azure_manager import AzureManager

powerbi_router = APIRouter()


@powerbi_router.post("/powerbi/embeded-token/")
async def generate_powerbi_token(request: GenerateEmbededTokenRequest):
    azure_manager = AzureManager()
    token = await azure_manager.get_powerbi_embeded_token(
        request.workspace_ids, request.dataset_ids, request.report_ids
    )
    return {"token": token}


@powerbi_router.get("/powerbi/reports/")
async def get_powerbi_reports():
    azure_manager = AzureManager()
    reports = await azure_manager.get_powerbi_reports()
    return {"reports": reports}


@powerbi_router.get("/powerbi/reports/{report_id}")
async def get_powerbi_report(report_id: str):
    azure_manager = AzureManager()
    report = await azure_manager.get_powerbi_report(report_id)
    return {"report": report}


@powerbi_router.get("/powerbi/workspaces/")
async def get_powerbi_workspaces():
    azure_manager = AzureManager()
    workspaces = await azure_manager.get_powerbi_workspaces()
    return {"workspaces": workspaces}
