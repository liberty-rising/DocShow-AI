from datetime import datetime
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class ResetTokenData(BaseModel):
    username: str
    exp: datetime


class EmailVerificationTokenData(BaseModel):
    email: str
    exp: datetime
