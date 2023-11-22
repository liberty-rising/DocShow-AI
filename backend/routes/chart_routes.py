from fastapi import APIRouter, HTTPException
from databases.dashboard_manager import DashboardManager
from databases.database_managers import ClientDatabaseManager
from models.client_models import Dashboard, DashboardCreate

import json
import os

chart_router = APIRouter()

@chart_router.get("/charts/types/")
async def get_chart_types():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'chart_types.json')
    with open(config_path, 'r') as file:
        chart_types = json.load(file)
    return chart_types
