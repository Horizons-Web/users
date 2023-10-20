from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    token: Optional[str]
    role: Optional[str]
    expiration_date: Optional[datetime]
    is_active: Optional[bool]
    user_id: Optional[int]


class ClientCreate(BaseModel):
    username: str
    email: str
    password: str
    dni: str
    physical_level: Optional[int] = None
    country: str
    administrative_area_level_1: str
    locality: str


class ClientCreated(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime


class ChangePassword(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str


class Login(BaseModel):
    username: str
    password: str
