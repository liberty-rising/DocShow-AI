from fastapi import APIRouter
from utils.azure.azure_manager import AzureManager

powerbi_router = APIRouter()


@powerbi_router.get("/powerbi/token/")
async def get_powerbi_token():
    azure_manager = AzureManager()
    token = azure_manager.get_powerbi_token()
    return {"token": token}


@powerbi_router.get("/powerbi/reports/")  # Uncomment this route
async def get_powerbi_reports():
    azure_manager = AzureManager()
    reports = azure_manager.get_powerbi_reports()
    return {"reports": reports}


@powerbi_router.get("/powerbi/reports/{report_id}")
async def get_powerbi_report(report_id: str):
    azure_manager = AzureManager()
    report = azure_manager.get_powerbi_report(report_id)
    return {"report": report}
