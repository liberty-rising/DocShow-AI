from fastapi import APIRouter, HTTPException
from databases.dashboard_manager import DashboardManager
from databases.database_managers import ClientDatabaseManager
from models.client.dashboard import Dashboard, DashboardCreate

dashboard_router = APIRouter()

@dashboard_router.get("/dashboard/")
async def get_dashboard(id: int):
    with ClientDatabaseManager() as session:
        manager = DashboardManager(session)
        dashboard = manager.get_dashboard(id)
        if dashboard:
            return dashboard.to_dict()
        else:
            raise HTTPException(status_code=404, detail="Dashboard not found")

@dashboard_router.get("/dashboards/")
async def get_dashboards():
    with ClientDatabaseManager() as session:
        manager = DashboardManager(session)
        dashboards = manager.get_dashboards()
    
    return dashboards

@dashboard_router.post("/dashboard/")
async def save_dashboard(dashboard: DashboardCreate):
    db_dashboard = Dashboard(
        name=dashboard.name,
        description=dashboard.description,
        organization=dashboard.organization
    )
    with ClientDatabaseManager() as session:
        manager = DashboardManager(session)
        manager.save_dashboard(db_dashboard)
