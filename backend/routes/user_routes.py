from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from models.user import (
    ChangePasswordRequest,
    DeleteUserRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    SendVerificationEmailRequest,
    User,
    UserOut,
    UserRole,
    UserUpdate,
    VerifyEmailRequest,
)
from database.database_manager import DatabaseManager
from database.user_manager import UserManager
from security import (
    decode_email_verification_token,
    decode_reset_token,
    generate_email_verification_token,
    generate_password_reset_token,
    get_current_admin_user,
    get_current_user,
    get_password_hash,
    verify_password,
)
from utils.email import (
    send_password_reset_email_with_sendgrid,
    send_verification_email_with_sendgrid,
)

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
    user_out = UserOut(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        organization_id=current_user.organization_id,
        role=current_user.role,
        requires_password_update=current_user.requires_password_update,
    )
    return user_out


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
    change_password: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
):
    # Verify old password
    if not verify_password(change_password.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid old password")

    with DatabaseManager() as session:
        user_manager = UserManager(session)

        # Update user password
        new_hashed_password = get_password_hash(change_password.new_password)
        updated_user = user_manager.update_user_password(
            username=current_user.username,
            new_hashed_password=new_hashed_password,
        )

        if updated_user.requires_password_update:
            user_manager.update_user_requires_password_update(
                username=current_user.username, requires_password_update=False
            )

        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")

        return {
            "message": f"Successfully updated password for {updated_user.username}."
        }


@user_router.post("/users/forgot-password/")
async def forgot_password(
    request: ForgotPasswordRequest, background_tasks: BackgroundTasks
):
    # Get user by email
    with DatabaseManager() as session:
        user_manager = UserManager(session)
        user = user_manager.get_user_by_email(email=request.email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

    # Generate password reset token
    token = generate_password_reset_token(user.username)

    # Send password reset email
    background_tasks.add_task(
        send_password_reset_email_with_sendgrid, [user.email], token
    )

    return {"message": "Password reset email sent"}


@user_router.put("/users/reset-password/")
async def reset_password(request: ResetPasswordRequest):
    token_data = decode_reset_token(request.token)

    if request.new_password != request.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    with DatabaseManager() as session:
        user_manager = UserManager(session)

        # Update user password
        new_hashed_password = get_password_hash(request.new_password)
        updated_user = user_manager.update_user_password(
            username=token_data.username,
            new_hashed_password=new_hashed_password,
        )

        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")

        return {
            "message": f"Successfully updated password for {updated_user.username}."
        }


@user_router.post("/users/send-verification-email/")
async def send_verification_email(
    request: SendVerificationEmailRequest, background_tasks: BackgroundTasks
):
    with DatabaseManager() as session:
        user_manager = UserManager(session)
        user = user_manager.get_user_by_email(request.email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Generate a verification token and save it in the database
        token = generate_email_verification_token(user.email)
        user_manager.update_user_verification_token(
            username=user.username, verification_token=token
        )

        # Add a background task to send the email
        background_tasks.add_task(
            send_verification_email_with_sendgrid, user.email, token
        )

    return {"message": f"Verification email sent for {user.email}"}


@user_router.put("/users/verify-email/")
async def verify_email(request: VerifyEmailRequest):
    with DatabaseManager() as session:
        user_manager = UserManager(session)

        # Decode the token and get the user
        token_data = decode_email_verification_token(request.token)
        user = user_manager.get_user_by_email(token_data.email)

        # Verify the token
        if user.verification_token != request.token:
            raise HTTPException(status_code=400, detail="Invalid verification token")

        # Update the user's email_verified field
        user_manager.update_user_email_verified(username=user.username)

        return {"message": f"Successfully verified email for {user.email}."}


@user_router.get("/users/is-email-verified/")
async def is_user_verified(current_user: User = Depends(get_current_user)):
    return {"email_verified": current_user.email_verified}


@user_router.delete("/users/delete/")
async def delete_user(
    request: DeleteUserRequest,
    current_admin_user: User = Depends(get_current_admin_user),
):
    with DatabaseManager() as session:
        user_manager = UserManager(session)

        # Delete user
        deleted_user = user_manager.delete_user_by_username(request.username)

        if not deleted_user:
            raise HTTPException(status_code=404, detail="User not found")

        return {"message": f"Successfully deleted user {request.username}."}
