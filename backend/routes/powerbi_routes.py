from fastapi import APIRouter
from utils.azure.azure_manager import AzureManager

powerbi_router = APIRouter()


@powerbi_router.get("/powerbi/token/")
async def get_powerbi_token():
    azure_manager = AzureManager()
    token = azure_manager.get_powerbi_token()
    return {"token": token}
