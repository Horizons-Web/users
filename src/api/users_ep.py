from fastapi import Depends, status, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse


from src.schema import user_schema, token_schema
from src.service import user_service

router = APIRouter(
    prefix="/api",
    tags=['Users']
)
token_auth_scheme = HTTPBearer()


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=user_schema.CreateResponse)
async def signup(user: user_schema.CreateRequest):
    """
    Create a new user
    """
    signup_response = await user_service.signup(user)
    return signup_response


@router.get("/confirm/{token}", status_code=status.HTTP_200_OK, response_model=None)
def confirm_user(token: str):
    """
    Confirm user email
    """
    confirmation_response = user_service.confirm_email(token)
    if confirmation_response:
        return RedirectResponse(url='https://frontend-3bsgyuggyq-ue.a.run.app/login')

@router.post("/login", status_code=status.HTTP_200_OK, response_model=str)
def login(user_credentials: user_schema.Login):
    """"
    user login
    """
    login_response = user_service.login(user_credentials)
    return "none"


@router.post("/logout", status_code=status.HTTP_200_OK, response_model=None)
def logout(token: HTTPAuthorizationCredentials = Depends(token_auth_scheme)):
    """
    Logout user
    """
    response = user_service.logout(token.credentials)
    return response


@router.post("/auth", status_code=status.HTTP_200_OK)
def authenticate(auth_request: token_schema.Auth):
    """
    Authenticate user
    """
    response = user_service.authenticate(auth_request)
    return response

@router.get("/logout", status_code=status.HTTP_200_OK)
def logout(token: HTTPAuthorizationCredentials = Depends(token_auth_scheme)):
    """
    Logout user
    """
    response = user_service.logout(token.credentials)
    return response
