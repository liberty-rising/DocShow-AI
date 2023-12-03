from fastapi import APIRouter, Depends, HTTPException
from security import get_current_admin_user, get_current_user, oauth2_scheme
from typing import Annotated

from models.user import User, UserOut, UserRole, UserUpdate
from databases.database_manager import DatabaseManager
from databases.user_manager import UserManager

user_router = APIRouter()


@user_router.get("/users/")
async def get_users(current_admin_user: User = Depends(get_current_admin_user)):
    # Open a database session and fetch all users
    with DatabaseManager() as session:
        user_manager = UserManager(session)
        users = user_manager.get_users_without_password()

    return users


@user_router.get("/users/me/", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_user)):
    current_user = get_current_user()
    return current_user


@user_router.get("/users/roles/")
async def get_user_roles(current_user: User = Depends(get_current_user)):
    return list(UserRole)


@user_router.put("/users/update/")
async def update_user(
    user_data: UserUpdate, current_admin_user: User = Depends(get_current_admin_user)
):
    with DatabaseManager() as session:
        user_manager = UserManager(session)

        # Update user details
        updated_user = user_manager.update_user_by_username(
            username=user_data.username,
            organization_id=user_data.organization_id,
            role=user_data.role,
        )

        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")

        return {"message": f"Successfully updated details for {user_data.username}."}
