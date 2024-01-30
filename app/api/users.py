from fastapi import Depends, status, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.schema import schema
from app.service import service
from app.repository import repository

token_auth_scheme = HTTPBearer()

router = APIRouter(
    prefix="/api",
    tags=['Users']
)



@router.post("/login", status_code=status.HTTP_200_OK)
def login(user_credentials: schema.Login, db: Session = Depends(repository.get_db)):
    '''
    Identifica y da acceso a usuarios
    '''
    response = service.login(user_credentials.username, user_credentials.password, db)

    return response


@router.post("/signup-client", status_code=status.HTTP_201_CREATED,)
def create_client(client_create: schema.ClientCreate, db: Session = Depends(repository.get_db)):
    '''
    Crea un usuario del tipo cliente
    '''
    response = service.signup_client(client_create, db)

    return response


@router.post("/signup-guide", status_code=status.HTTP_201_CREATED)
def create_guide(guide_create: schema.GuideCreate, db: Session = Depends(repository.get_db)):
    '''
    Crea un usuario del tipo guia
    '''
    response = service.signup_guide(guide_create, db)
 
    return response


@router.get("/confirm/", status_code=status.HTTP_200_OK)
def confirm_user(token: str, db: Session = Depends(repository.get_db)):
    '''
    Confirma la cuenta de usuarios
    '''
    response = service.confirm_email(token, db)

    return response


@router.put("/change-password", status_code=status.HTTP_200_OK)
def change_password(password: schema.ChangePassword, token: HTTPAuthorizationCredentials = Depends(token_auth_scheme), db: Session = Depends(repository.get_db)):
    '''
    Cambia la contrasena usuarios
    '''
    response = service.change_password(password, token.credentials, db)

    return response


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(token: HTTPAuthorizationCredentials = Depends(token_auth_scheme), db: Session = Depends(repository.get_db)):
    '''
    Revoca acceso a un usuario
    '''
    response = service.logout(token.credentials, db)

    return response


@router.post("/auth", status_code=status.HTTP_200_OK)
def authenticate(auth_request: schema.Auth, db: Session = Depends(repository.get_db)):
    '''
    Autentica usuarios
    '''
    response = service.authenticate(auth_request, db)

    return response
