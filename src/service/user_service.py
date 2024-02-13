from fastapi.exceptions import HTTPException
from fastapi import status

from datetime import timedelta

from src.repository import user_repository
from src.schema import user_schema, token_schema
from src.utils.utils import _hash, send_confirmation_email, create_confirmation_token, decode_token, verify
from src.utils import errors
from src.auth import auth


async def signup(user: user_schema.CreateRequest):
    try:
        confirmation_token = create_confirmation_token(user.email, expires_delta=timedelta(hours=24))
        await send_confirmation_email(user.email, confirmation_token)
        hashed_password = _hash(user.password)
        user.password = hashed_password
        repository = user_repository.UserRepository()
        signup_response = repository.create(user)
        return signup_response
    except errors.EmailSendError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error sending email")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating user")


def confirm_email(token: str):
    try:
        payload = decode_token(token)
        email = payload.get("email")
        params = user_schema.Params(email=email)
        update = user_schema.Update(is_active=True)
        repository = user_repository.UserRepository()
        repository.put(params, update)
        return {"message": "Email confirmed successfully"}
    except errors.UserNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found with this email")
    except errors.UpdateError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error confirming email")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error confirming email")


def login(user_credentials: user_schema.Login):
    try:
        _user_repository = user_repository.UserRepository()
        _token_repository = user_repository.TokenRepository()
        user = _user_repository.get(user_schema.Params(username=user_credentials.username))
        hashed_password = user.password
        verify(user_credentials.password, hashed_password)
        token_exist = _token_repository.get(token_schema.Params(user_id=user.id, exists=True))
        if user.is_active is False:
            raise errors.UserNotActive("User not active")
        if token_exist is None:
            return str(_token_repository.create(auth.create_access_token(user.id, user.user_type)).token)
        else:
            return str(_token_repository.update(auth.create_access_token(user.id, user.user_type)).token)

    except errors.UserNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except errors.InvalidCredentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    except errors.UserNotActive:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not active")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error logging in")



def authenticate(auth_request: token_schema.Auth):
    try:
        repository = user_repository.TokenRepository()
        token_db = repository.get(token_schema.Params(token=auth_request.token))
        if token_db.is_active is False:
            raise errors.TokenNotActive
        return auth.verify_token(auth_request.token, auth_request.role_request)

    except errors.TokenNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Token not found")
    except errors.TokenNotActive:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token not active")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error authenticating")


def logout(token: str):
    try:
        token_data = auth.verify_token(token, "public")
        repository = user_repository.TokenRepository()
        repository.update(token_schema.Data(user_id=token_data.user_id, is_active=False))
        return {"message": "Logged out successfully"}

    except errors.TokenNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Token not found")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error logging out")

"""""

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



 



"""
