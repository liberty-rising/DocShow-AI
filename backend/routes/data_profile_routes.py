from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .databases import SessionLocal, DataProfileManager

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/data-profiles/")
async def get_data_profiles(db: Session = Depends(get_db)):
    data_profile_manager = DataProfileManager(db)
    return data_profile_manager.get_all_data_profiles()