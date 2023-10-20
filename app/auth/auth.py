from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import status, HTTPException
from fastapi.security import HTTPBearer

from app.schema import schema
from app.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

token_auth_scheme = HTTPBearer()


def create_access_token(data: schema.TokenData):
    exp = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.dict()
    to_encode["expiration_date"] = str(exp)
    to_encode["is_active"] = True
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    data.token = encoded_jwt
    data.expiration_date = exp

    return data


def verify_role(user_role: str, role_request: str):

    if user_role == role_request:
        return True
    if role_request == 'public':
        return True

    return False


def verify_token(token: str, role_request: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user: int = payload.get("user_id")
        expiration_date_str: str = payload.get("expiration_date")
        expiration_date = datetime.strptime(expiration_date_str, "%Y-%m-%d %H:%M:%S.%f")
        is_active: bool = payload.get("is_active")
        role: str = payload.get("role")

        if user is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No posees credenciales")
        if expiration_date < datetime.utcnow():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="El token expiro")
        if not is_active:
            print(payload.get("is_active"))
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token invalido")
        if not verify_role(role, role_request):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No posees los permisos requeridos")

        token_data = schema.TokenData(
            token=payload.get("token"),
            role=payload.get("role"),
            expiration_date=payload.get("expiration_date"),
            is_active=payload.get("is_active"),
            user_id=payload.get("user_id")
        )

    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se pudo decodificar el token")

    return token_data
