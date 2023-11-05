from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    token: str
    expiration_date: str
    is_active: bool
    user_id: int
    role: str


class TokenCreate(BaseModel):
    user_id: int
    role: str


class ClientCreate(BaseModel):
    username: str
    email: str
    password: str
    dni: str
    physical_level: Optional[int] = None
    country: str
    administrative_area_level_1: str
    locality: str


class GuideCreate(BaseModel):
    username: str
    email: str
    password: str
    dni: str
    country: str
    administrative_area_level_1: str
    locality: str


class UserCreated(BaseModel):
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

class Auth(BaseModel):
    token: str
    role_request: str