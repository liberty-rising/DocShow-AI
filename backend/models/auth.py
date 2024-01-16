from typing import Optional

from pydantic import BaseModel, EmailStr


class CustomOAuth2PasswordRequestForm(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": None,
                "password": "secret",
            }
        }
