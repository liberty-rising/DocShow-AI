from fastapi import APIRouter
from databases.dashboard_manager import DashboardManager
from databases.database_managers import ClientDatabaseManager
from models.client_models import Dashboard, DashboardCreate

dashboard_router = APIRouter()

@dashboard_router.get("/dashboard/")
async def get_dashboard(id: int):
    with ClientDatabaseManager() as session:
        manager = DashboardManager(session)
        dashboard = manager.get_dashboard(id)
    
    return dashboard

@dashboard_router.get("/dashboards/")
async def get_dashboards():
    with ClientDatabaseManager() as session:
        manager = DashboardManager(session)
        dashboards = manager.get_dashboards()
    
    return dashboards

@dashboard_router.post("/dashboard/")
async def create_dashboard(dashboard: DashboardCreate):
    db_dashboard = Dashboard(
        name=dashboard.name,
        description=dashboard.description,
        organization=dashboard.organization
    )
    with ClientDatabaseManager() as session:
        manager = DashboardManager(session)
        manager.create_dashboard(db_dashboard)
