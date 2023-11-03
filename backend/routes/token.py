from databases.database_managers import AppDatabaseManager
from databases.user_manager import UserManager
from models.app_models import Token, TokenData, User, UserCreate
from security import create_access_token, verify_password, get_password_hash
from settings import ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/token/", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    with AppDatabaseManager() as session:
        user_manager = UserManager(session)
        user = user_manager.get_user(username=form_data.username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register/", response_model=Token)
async def register(user: UserCreate):
    with AppDatabaseManager() as session:
        user_manager = UserManager(session)
        
        # Check if username or email is already registered
        existing_user = user_manager.get_user(username=user.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        existing_email = user_manager.get_email(email=user.email)
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Hash the user's password
        hashed_password = get_password_hash(user.password)
        
        # Store the user details in the database
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password
        )
        user_manager.create_user(db_user)
        
        # Optionally, auto-login the user and return a token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}