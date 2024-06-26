"""
This module provides routes for token-based user authentication and registration using FastAPI.
It integrates with a database manager to perform CRUD operations on the User model and leverages
the security module for creating JWT tokens and password hashing/verification.
"""
from datetime import timedelta
from typing import Optional

from database.database_manager import DatabaseManager
from database.user_manager import UserManager
from fastapi import APIRouter, Depends, Form, HTTPException, Response, status
from models.auth import CustomOAuth2PasswordRequestForm
from models.user import User, UserCreate
from pydantic import BaseModel, EmailStr
from security import (
    authenticate_user,
    create_token,
    get_current_user,
    get_password_hash,
    set_tokens_in_cookies,
    update_user_refresh_token,
    verify_refresh_token,
)
from settings import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
    REMEMBER_ME_ACCESS_TOKEN_EXPIRE_MINUTES,
    REMEMBER_ME_REFRESH_TOKEN_EXPIRE_DAYS,
)

auth_router = APIRouter()


class LoginResponse(BaseModel):
    message: str


class RegistrationResponse(BaseModel):
    message: str


class LogoutResponse(BaseModel):
    message: str


@auth_router.post("/token/", response_model=LoginResponse)
async def login_for_access_token(
    response: Response,
    username: Optional[str] = Form(None),
    email: Optional[EmailStr] = Form(None),
    password: str = Form(...),
    remember: bool = Form(False),
):
    """
    Authenticate a user and set a JWT token in a cookie upon successful authentication.

    This endpoint verifies the provided username and password. If the credentials are valid,
    it creates a JWT token and sets it in a secure, HttpOnly cookie in the response.

    Args:
        form_data (CustomOAuth2PasswordRequestForm): Contains the user's provided username/email and password.

    Returns:
        dict: A success message indicating successful authentication. The JWT token is not returned in the response body but is set in a secure cookie.
    """
    form_data = CustomOAuth2PasswordRequestForm(
        username=username, email=email, password=password
    )
    user = authenticate_user(form_data.username, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if remember:
        access_token = create_token(
            {"sub": user.username},
            timedelta(minutes=REMEMBER_ME_ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        refresh_token = create_token(
            {"sub": user.username},
            timedelta(days=REMEMBER_ME_REFRESH_TOKEN_EXPIRE_DAYS),
        )
    else:
        access_token = create_token(
            {"sub": user.username},
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        refresh_token = create_token(
            {"sub": user.username}, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        )
    update_user_refresh_token(
        user_id=user.id,
        refresh_token=refresh_token,
    )

    set_tokens_in_cookies(response, access_token, refresh_token)
    return {"message": "Login successful"}


@auth_router.post("/refresh-token/")
async def refresh_access_token(
    response: Response, user: User = Depends(verify_refresh_token)
):
    """
    Refresh the access token using a valid refresh token.

    This endpoint reads the refresh token from a cookie, verifies it, and then
    issues a new access token and a new refresh token. The new tokens are set
    in secure, HttpOnly cookies in the response.

    Args:
        user (User): The user object obtained from the verified refresh token.

    Returns:
        dict: A message indicating successful token refresh. The new tokens are not returned in the response body but are set in secure cookies.
    """

    # Ensure the user is valid
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    access_token = create_token(
        {"sub": user.username},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    new_refresh_token = create_token(
        {"sub": user.username}, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    update_user_refresh_token(
        user_id=user.id,
        refresh_token=new_refresh_token,
    )

    set_tokens_in_cookies(response, access_token, new_refresh_token)


@auth_router.get("/verify-token/", response_model=dict)
async def verify_token(current_user: User = Depends(get_current_user)):
    """
    Verify the JWT token and confirm the user is logged in.

    Returns:
        dict: A confirmation message if the user is authenticated.
    """
    # Assuming current_user is valid, return confirmation
    if current_user:
        return {"message": "User is authenticated"}
    else:
        # If for any reason current_user is None or invalid
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User authentication failed",
        )


@auth_router.post("/register/", response_model=RegistrationResponse)
async def register(response: Response, user_create_request: UserCreate):
    """
    Register a new user and set a JWT token in a cookie upon successful registration.

    This endpoint registers a new user with the provided details. It checks for the uniqueness of the username and email. If the registration is successful, it creates a JWT token,
    sets it in a secure, HttpOnly cookie in the response, and returns a success message.

    Args:
        user_create_request (UserCreate): Pydantic model containing the user's registration details, such as username, email, and password.

    Returns:
        dict: A success message indicating successful registration. The JWT token is not returned in the response body but is set in a secure cookie.
    """
    with DatabaseManager() as session:
        user_manager = UserManager(session)

        # Ensure unique username and email
        existing_user = user_manager.get_user_by_username(
            username=user_create_request.username
        )
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        existing_email = user_manager.get_email(email=user_create_request.email)
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Hash the user's password
        hashed_password = get_password_hash(user_create_request.password)

        # Add user to the database
        db_user = User(
            username=user_create_request.username,
            email=user_create_request.email,
            hashed_password=hashed_password,
            subscribe_to_updates=user_create_request.subscribe_to_updates,
            receive_marketing_content=user_create_request.receive_marketing_content,
            requires_password_update=user_create_request.requires_password_update,
        )
        new_user = user_manager.create_user(db_user)

        # Generate access token
        access_token = create_token(
            {"sub": new_user.username},
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        refresh_token = create_token(
            {"sub": new_user.username}, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        )

        update_user_refresh_token(
            user_id=new_user.id,
            refresh_token=refresh_token,
        )

        set_tokens_in_cookies(response, access_token, refresh_token)
        return {"message": "Registration successful"}


@auth_router.post("/logout/", response_model=LogoutResponse)
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"message": "Logged out successfully"}
