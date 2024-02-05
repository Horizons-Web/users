from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class Params(BaseModel):
    user_id: Optional[UUID4] = None
    token: Optional[str] = None
    exists: Optional[bool] = None


class Data(BaseModel):
    token: Optional[str] = None
    expiration_date: Optional[datetime] = None
    is_active: Optional[bool] = None
    user_id: Optional[UUID4] = None
    role: Optional[str] = None


class Create(BaseModel):
    user_id: UUID4
    role: str


class Auth(BaseModel):
    token: str
    role_request: str
