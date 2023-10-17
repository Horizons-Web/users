from fastapi import Depends, status, HTTPException, APIRouter
from fastapi.security import HTTPBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from ..auth import auth
from ..schema import schema
from ..utils.utils import hash, verify
from ..utils.email import send_confirmation_email, create_confirmation_token, decode_token
from ..repository import repository

token_auth_scheme = HTTPBearer()

router = APIRouter(
    prefix="/api/users",
    tags=['Users']
)


@router.post(
    "/login", status_code=status.HTTP_200_OK
)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(repository.get_db)):

    user = repository.get_user_by_username(db, user_credentials.username)
    if user is None:
        raise (
            HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credenciales incorrectas")
        )

    hashed_password = repository.get_password_by_username(db, user_credentials.username)
    if not verify(user_credentials.password, hashed_password):
        raise (
            HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credenciales incorrectas")
        )

    access_token = auth.create_access_token(data={"user_id": user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post(
    "/clients", status_code=status.HTTP_201_CREATED, response_model=schema.ClientCreated
)
def create_client(client_create: schema.ClientCreate, db: Session = Depends(repository.get_db)):
    username = repository.get_user_by_username(db, client_create.username)
    if username is not None:
        raise (
            HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un usuario con este nombre")
        )

    email = repository.get_user_by_email(db, client_create.email)
    if email is not None:
        raise (
            HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un usuario con este email")
        )

    dni = repository.get_client_by_dni(db, client_create.dni)
    if dni is not None:
        raise (
            HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un usuario con este dni")
        )

    hashed_password = hash(client_create.password)
    client_create.password = hashed_password

    confirmation_token = create_confirmation_token(
        data={"email": client_create.email},
        expires_delta=timedelta(hours=24)
    )
    send_confirmation_email(client_create.email, confirmation_token)

    return repository.create_client(db, client_create)


@router.get("/confirm/", status_code=status.HTTP_200_OK)
def confirm_user(token: str, db: Session = Depends(repository.get_db)):
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")

    email = payload.get("email")
    id_to_confirm = repository.get_user_by_email(db, email).id
    repository.activate_user(db, id_to_confirm)

    return {"message": "User confirmed"}


@router.put("/change-password", status_code=status.HTTP_200_OK)
def change_password(
        password: schema.ChangePassword,
        db: Session = Depends(repository.get_db),
        current_user: schema.TokenData = Depends(auth.get_current_user)
):

    if password.new_password != password.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Las contraseñas no coinciden")

    hashed_password = repository.get_password_by_id(db, current_user.id)

    if not verify(password.current_password, hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Contraseña actual incorrecta")

    hashed_new_password = hash(password.new_password)
    repository.change_password(db, current_user.id, hashed_new_password)

    return {"message": "Contraseña actualizada correctamente"}