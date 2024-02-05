from fastapi import status, HTTPException
from fastapi.security import HTTPBearer

from jose import JWTError, jwt

from datetime import datetime, timedelta

from app.schema import token_schema
from app.config import settings
from app.utils import errors


token_auth_scheme = HTTPBearer()


def create_access_token(user_id: int, user_type: str):
    exp = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "expiration_date": str(exp),
        "is_active": True,
        "user_id": user_id,
        "role": user_type
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    data = token_schema.Data(
        token=encoded_jwt,
        expiration_date=str(exp),
        is_active=True,
        user_id=user_id,
        role=user_type
    )
    return data


def verify_role(user_role: str, role_request: str):
    if user_role == role_request:
        return True
    if role_request == 'public':
        return True
    return False


def verify_token(token: str, role_request: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user: int = payload.get("user_id")
        expiration_date_str: str = payload.get("expiration_date")
        expiration_date = datetime.strptime(expiration_date_str, "%Y-%m-%d %H:%M:%S.%f")
        is_active: bool = payload.get("is_active")
        role: str = payload.get("role")
        if user is None:
            raise errors.TokenNotFound
        if expiration_date < datetime.utcnow():
            raise errors.TokenExpired
        if not is_active:
            raise errors.TokenNotActive
        if not verify_role(role, role_request):
            raise errors.PermissionDenied
        token_data = token_schema.Data(
            token=token,
            role=payload.get("role"),
            expiration_date=payload.get("expiration_date"),
            is_active=payload.get("is_active"),
            user_id=payload.get("user_id")
        )
        return token_data
    except JWTError:
        raise errors.JWTError
