from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, Request, status
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

def get_password_hash(password):
    """
    Generate a hashed version of the provided password.
    
    Args:
        password: The plain text password.
    
    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """
    Create an access JWT token.
    
    Args:
        data: Data to encode into the token.
        expires_delta: Time duration for the token to remain valid. Defaults to 15 minutes if not provided.
    
    Returns:
        str: The generated JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
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