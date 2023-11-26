"""
This module provides routes for token-based user authentication and registration using FastAPI. 
It integrates with a database manager to perform CRUD operations on the User model and leverages 
the security module for creating JWT tokens and password hashing/verification.
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from databases.database_managers import AppDatabaseManager
from databases.user_manager import UserManager
from models.app_models import Token, User, UserCreate
from security import authenticate_user, create_token, get_password_hash, set_tokens_in_cookies, verify_refresh_token, update_user_refresh_token
from settings import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS


auth_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class LoginResponse(BaseModel):
    message:str

class RegistrationResponse(BaseModel):
    message:str

class LogoutResponse(BaseModel):
    message:str

@auth_router.post("/token/", response_model=LoginResponse)
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate a user and set a JWT token in a cookie upon successful authentication. 
    
    This endpoint verifies the provided username and password. If the credentials are valid, 
    it creates a JWT token and sets it in a secure, HttpOnly cookie in the response.

    Args:
        form_data (OAuth2PasswordRequestForm): Contains the user's provided username and password.

    Returns:
        dict: A success message indicating successful authentication. The JWT token is not returned in the response body but is set in a secure cookie.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_token({"sub": user.username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_token({"sub": user.username}, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    update_user_refresh_token(user.id, refresh_token)

    set_tokens_in_cookies(response, access_token, refresh_token)
    return {"message": "Login successful"}

@auth_router.post("/refresh-token/")
async def refresh_access_token(response: Response, user: User = Depends(verify_refresh_token)):
    """
    Refresh the access token using a valid refresh token.

    Args:
        refresh_token (str): The refresh token provided by the user.

    Returns:
        dict: The new access token.
    """
    print("ATTEMPING TOKEN REFRESH")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    access_token = create_token({"sub": user.username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    new_refresh_token = create_token({"sub": user.username}, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

    update_user_refresh_token(user.id, new_refresh_token)

    set_tokens_in_cookies(response, access_token, new_refresh_token)

@auth_router.post("/register/", response_model=RegistrationResponse)
async def register(response: Response, user: UserCreate):
    """
    Register a new user and set a JWT token in a cookie upon successful registration.

    This endpoint registers a new user with the provided details. It checks for the uniqueness of the username and email. If the registration is successful, it creates a JWT token, sets it in a secure, HttpOnly cookie in the response, and returns a success message.

    Args:
        user (UserCreate): Pydantic model containing the user's registration details, such as username, email, and password.

    Returns:
        dict: A success message indicating successful registration. The JWT token is not returned in the response body but is set in a secure cookie.
    """
    with AppDatabaseManager() as session:
        user_manager = UserManager(session)
        
        # Ensure unique username and email
        existing_user = user_manager.get_user(username=user.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        existing_email = user_manager.get_email(email=user.email)
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Hash the user's password
        hashed_password = get_password_hash(user.password)
        
        # Add user to the database
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password
        )
        user_manager.create_user(db_user)
        
        # Generate access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )

        # Set cookie
        response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True, max_age=1800, secure=True, samesite='Lax')

        return {"message": "Registration successful"}

@auth_router.post("/logout/", response_model=LogoutResponse)
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logged out successfully"}
