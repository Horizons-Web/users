from fastapi import Depends
from datetime import timedelta
from sqlalchemy.orm import Session

from app.repository import repository
from app.schema import schema
from app.utils.utils import hash, verify
from app.utils.email import send_confirmation_email, create_confirmation_token, decode_token
from app.auth import auth





def login(username: str, password: str, db: Session):

    user = repository.get_user_by_username(db, username)

    if user is None:
        raise (
            HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
        )

    hashed_password = repository.get_password_by_username(db, username)

    if not verify(password, hashed_password):
        raise (
            HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
        )
    
    token_update = repository.get_token_by_user_id(db, user.id)
    
    token = auth.create_access_token(user.id, user.user_type)

    if token_update is None:
        return repository.create_token(db, token).token
    else:
        return repository.update_token(db, token).token


def signup_client(client_create: schema.ClientCreate, db: Session):


    username = repository.get_user_by_username(db, client_create.username)
    if username is not None:
        raise (
            HTTPException(status_code=status.HTTP_409_CONFLICT, detail="There is already a user with this name")
        )

    email = repository.get_user_by_email(db, client_create.email)
    if email is not None:
        raise (
            HTTPException(status_code=status.HTTP_409_CONFLICT, detail="There is already a user with this email")
        )

    dni = repository.get_client_by_dni(db, client_create.dni)
    if dni is not None:
        raise (
            HTTPException(status_code=status.HTTP_409_CONFLICT, detail="There is already a user with this DNI")
        )

    hashed_password = hash(client_create.password)
    client_create.password = hashed_password

    confirmation_token = create_confirmation_token(
        data={"email": client_create.email},
        expires_delta=timedelta(hours=24)
    )
    send_confirmation_email(client_create.email, confirmation_token)

    return repository.create_client(db, client_create)


def signup_guide(guide_create: schema.GuideCreate, db: Session):

    username = repository.get_user_by_username(db, guide_create.username)
    if username is not None:
        raise (
            HTTPException(status_code=status.HTTP_409_CONFLICT, detail="There is already a user with this name")
        )

    email = repository.get_user_by_email(db, guide_create.email)
    if email is not None:
        raise (
            HTTPException(status_code=status.HTTP_409_CONFLICT, detail="There is already a user with this email")
        )

    hashed_password = hash(guide_create.password)
    guide_create.password = hashed_password

    confirmation_token = create_confirmation_token(
        data={"email": guide_create.email},
        expires_delta=timedelta(hours=24)
    )
    send_confirmation_email(guide_create.email, confirmation_token)

    return repository.create_guide(db, guide_create)


def confirm_email(token: str, db: Session):

    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")

    email = payload.get("email")
    id_to_confirm = repository.get_user_by_email(db, email).id
    repository.activate_user(db, id_to_confirm)

    return {"message": "User confirmed"}  


def change_password(password: schema.ChangePassword, token: str, db: Session):

    if repository.get_token_by_token(db, token.credentials) is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    token_data = auth.verify_token(token.credentials, "public")
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    if password.new_password != password.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords not match"
        )

    if not verify(password.current_password, repository.get_password_by_id(db, token_data.user_id)):
        raise (
            HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid password")
        )

    repository.change_password(db, token_data.user_id, hash(password.new_password))   


def logout(token: str, db: Session):

    token_data = auth.verify_token(token, "public")
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    return repository.deactivate_token(db, token_data.user_id)
 

def authenticate(auth_request: schema.Auth, db: Session):

    token_db = repository.get_token_by_token(db, auth_request.token)
    if token_db is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    if token_db is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token deactivated"
        )

    return auth.verify_token(auth_request.token, auth_request.role_request)

