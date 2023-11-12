from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from security import get_current_user
from models.app_models import User
from superset.superset_manager import SupersetManager
from superset.utils import get_superset_manager

superset_router = APIRouter()

@superset_router.get("/dashboard/{dashboard_id}")
async def get_dashboard(dashboard_id: int, current_user: User = Depends(get_current_user)):
    # TODO: Implement user-specific logic for current_user.
    
    superset_manager = get_superset_manager(current_user)
    
    try:
        response = superset_manager.get_dashboard_by_id(dashboard_id)
        print(response)
        return Response(content=response.content, media_type=response.headers['Content-Type'])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@superset_router.get("/dashboards/")
async def list_dashboards(superset_manager: SupersetManager = Depends(get_superset_manager)):
    try:
        dashboards = superset_manager.list_dashboards()
        return {"dashboards": dashboards}
    except Exception as e:
        return {"error": str(e)}