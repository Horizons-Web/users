from pydantic import BaseModel, UUID4, EmailStr, Field, validator
from datetime import datetime
from typing import Optional


class CreateRequest(BaseModel):
    username: str = Field(min_length=3, max_length=30, default="username")
    email: EmailStr = "joaquinreyero12@gmail.com"
    password: str = Field(min_length=8, default="password")
    user_type: str = "guide"

    @validator('user_type')
    def validate_user_type(cls, v):
        if v not in ['guide', 'client']:
            raise ValueError("user_type must be 'guide' or 'client'")
        return v

    class Config:
        orm_mode = True


class CreateResponse(BaseModel):
    id: UUID4
    username: str
    email: EmailStr
    created_at: datetime


class Update(BaseModel):
    username: Optional[str] = Field(min_length=3, max_length=30, default=None)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(min_length=8, default=None)
    is_active: Optional[bool] = None

    class Config:
        orm_mode = True


class Params(BaseModel):
    id: Optional[UUID4] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class Login(BaseModel):
    username: str = "username"
    password: str = "password"


class GetUser(BaseModel):
    id: str
    username: str
    email: EmailStr
    password: str
    user_type: str
    is_active: bool
    address_id: str

