from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from typing import Any, Union

from databases.database_managers import AppDatabaseManager
from databases.user_manager import UserManager
from models.app_models import User
from settings import JWT_SECRET_KEY


# Configuration for JWT token
ALGORITHM = "HS256"  # HMAC SHA-256

# Setup for OAuth2 password-based token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token/")

# Context for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate_user(username: str, password: str) -> User:
    with AppDatabaseManager() as session:
        manager = UserManager(session)
        user = manager.get_user(username)
        if user and verify_password(password, user.hashed_password):
            return user
        return None

def verify_password(plain_password, hashed_password):
    """
    Verify a password using its hashed version.
    
    Args:
        plain_password: The plain text password.
        hashed_password: The hashed version of the password.
    
    Returns:
        bool: True if password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def verify_refresh_token(token: str = Depends(oauth2_scheme)) -> User:
    """
    Verify a refresh token and return the associated user.

    Args:
        token (str): The refresh token to verify.

    Returns:
        User: The user associated with the valid refresh token.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    try:
        # Decode the token
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        # Find the user in the database
        with AppDatabaseManager() as session:
            manager = UserManager(session)
            user = manager.get_user(username)

        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        # Verify the token matches the user's stored refresh token
        if user.refresh_token != token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        return user.refresh_token
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def get_password_hash(password):
    """
    Generate a hashed version of the provided password.
    
    Args:
        password: The plain text password.
    
    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)

def create_token(data: dict, expires_delta: timedelta) -> str:
    """
    Create an  JWT token.
    
    Args:
        data: Data to encode into the token.
        expires_delta: Time duration for the token to remain valid.
    
    Returns:
        str: The generated JWT token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    """
    Decode a JWT token.
    
    Args:
        token: The JWT token to decode.
    
    Returns:
        dict: The decoded payload if successful.
        None: If decoding fails.
    """
    try:
        token = token.replace("Bearer ", "", 1)  # Remove Bearer prefix
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def get_current_user(request: Request) -> User:
    """
    Retrieve the current user based on the JWT token stored in the cookie.
    
    Args:
        request (Request): The request object.
    
    Returns:
        User: The user object associated with the token.
    
    Raises:
        HTTPException: If token is invalid or user is not found.
    """
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Not authenticated"
        )

    try:
        payload = decode_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    with AppDatabaseManager() as session:
        user_manager = UserManager(session)
        user = user_manager.get_user(username=username)
        
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user

def set_tokens_in_cookies(response: Response, access_token: str, refresh_token: str):
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", 
        httponly=True, max_age=1800, secure=True, samesite='Lax'
    )
    response.set_cookie(
        key="refresh_token", value=f"Bearer {refresh_token}", 
        httponly=True, max_age=60*60*24*7, secure=True, samesite='Lax'
    )

def update_user_refresh_token(user_id: int, refresh_token: str):
    with AppDatabaseManager() as session:
        manager = UserManager(session)
        manager.update_user(user_id, refresh_token=refresh_token)