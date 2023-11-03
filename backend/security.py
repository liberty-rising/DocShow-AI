from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from typing import Any, Union

from databases.database_managers import AppDatabaseManager
from databases.user_manager import UserManager
from models.app_models import TokenData

import os

# Configuration for JWT token
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'mysecretkey')
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
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Retrieve the current user based on the JWT token.
    
    Args:
        token: The JWT token.
    
    Returns:
        User: The user object associated with the token.
    
    Raises:
        HTTPException: If token is invalid or user is not found.
    """
    payload = decode_token(token)
    if payload is None or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Token has expired or is invalid. Please log in again."
        )
    
    username = payload["sub"]

    with AppDatabaseManager() as session:
        user_manager = UserManager(session)
        user = user_manager.get_user(username=username)
        
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user