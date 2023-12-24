from fastapi import APIRouter, Depends, HTTPException
from security import (
    get_current_admin_user,
    get_current_user,
    get_password_hash,
    verify_password,
)

from models.user import ChangePassword, User, UserOut, UserRole, UserUpdate
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


@user_router.put("/users/change-password/")
async def change_user_password(
    change_password: ChangePassword, current_user: User = Depends(get_current_user)
):
    print("change_password", change_password)
    # Verify old password
    if not verify_password(change_password.old_password, current_user.hashed_password):
        print("HELLO")
        raise HTTPException(status_code=400, detail="Invalid old password")

    with DatabaseManager() as session:
        user_manager = UserManager(session)

        # Update user password
        new_hashed_password = get_password_hash(change_password.new_password)
        updated_user = user_manager.update_user_password(
            username=current_user.username,
            new_hashed_password=new_hashed_password,
        )

        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")

        return {
            "message": f"Successfully updated password for {updated_user.username}."
        }
