from fastapi import Depends, status, HTTPException, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import timedelta

from app.auth import auth
from app.schema import schema
from app.utils.utils import hash, verify
from app.utils.email import send_confirmation_email, create_confirmation_token, decode_token
from app.repository import repository

token_auth_scheme = HTTPBearer()

router = APIRouter(
    prefix="/api/users",
    tags=['Users']
)


@router.get(
    "/test", status_code=status.HTTP_200_OK
)
def test():
    return {"message":"Hola desde users!"}


@router.post(
    "/login", status_code=status.HTTP_200_OK
)
def login(user_credentials: schema.Login, db: Session = Depends(repository.get_db)):
    user = repository.get_user_by_username(db, user_credentials.username)
    if user is None:
        raise (
            HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credenciales incorrectas")
        )

    hashed_password = repository.get_password_by_username(db, user_credentials.username)
    print(user_credentials.password)
    print(hashed_password)
    if not verify(user_credentials.password, hashed_password):
        raise (
            HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credenciales incorrectas")
        )

    token = schema.TokenData(
        user_id=user.id,
        role=user.user_type,
    )

    token_update = repository.get_token_by_user_id(db, user.id)

    token = auth.create_access_token(token)

    if token_update is None:
        return repository.create_token(db, token).token
    else:
        return repository.update_token(db, token).token


@router.post(
    "/signup", status_code=status.HTTP_201_CREATED, response_model=schema.ClientCreated
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
        token: HTTPAuthorizationCredentials = Depends(token_auth_scheme)
):
    token_data = auth.verify_token(token.credentials, "public")
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales invalidas"
        )

    if password.new_password != password.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Las contraseñas no coinciden"
        )

    if not verify(password.current_password, repository.get_password_by_id(db, token_data.user_id)):
        raise (
            HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="contraseña incorrecta")
        )

    repository.change_password(db, token_data.user_id, hash(password.new_password))


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(
        token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
        db: Session = Depends(repository.get_db),

):
    token_data = auth.verify_token(token.credentials, "public")
    if token_data is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales invalidas")

    return repository.deactivate_token(db, token_data.user_id)
