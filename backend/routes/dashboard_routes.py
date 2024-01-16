from database.dashboard_manager import DashboardManager
from database.database_manager import DatabaseManager
from fastapi import APIRouter, Depends, HTTPException
from models.dashboard import Dashboard, DashboardCreate
from models.user import User
from security import get_current_user

dashboard_router = APIRouter()


@dashboard_router.get("/dashboard/")
async def get_dashboard(id: int, current_user: User = Depends(get_current_user)):
    with DatabaseManager() as session:
        manager = DashboardManager(session)
        dashboard = manager.get_dashboard(id)
        if dashboard:
            return dashboard.to_dict()
        else:
            raise HTTPException(status_code=404, detail="Dashboard not found")


@dashboard_router.get("/dashboards/")
async def get_dashboards(current_user: User = Depends(get_current_user)):
    with DatabaseManager() as session:
        manager = DashboardManager(session)
        dashboards = manager.get_dashboards()

    return dashboards


@dashboard_router.post("/dashboard/")
async def save_dashboard(
    dashboard: DashboardCreate, current_user: User = Depends(get_current_user)
):
    db_dashboard = Dashboard(
        name=dashboard.name,
        description=dashboard.description,
        organization=dashboard.organization,
    )
    with DatabaseManager() as session:
        manager = DashboardManager(session)
        manager.save_dashboard(db_dashboard)
