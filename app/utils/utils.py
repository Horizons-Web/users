from fastapi_mail import FastMail, MessageSchema, MessageType


from jose import JWTError, jwt
from passlib.context import CryptContext

from datetime import datetime, timedelta

from app.config import settings, configure_mail
from app.utils import errors

smtp_use_ssl = True
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    verified = pwd_context.verify(plain_password, hashed_password)
    if not verified:
        raise errors.InvalidCredentials("Invalid credentials")
    return


async def send_confirmation_email(email: str, confirmation_token: str):
    html = """
    <p>Click on the link to confirm your email</p> 
    <a href="{0}/api/confirm/{1}">Confirm email</a>
    """.format(settings.USERS_LOCALHOST, confirmation_token)
    message = MessageSchema(
        subject="Email confirmation",
        recipients=[email],
        body=html,
        subtype=MessageType.html
    )
    fm = FastMail(configure_mail())
    await fm.send_message(message)


def create_confirmation_token(data: str, expires_delta: timedelta):
    expire = datetime.utcnow() + expires_delta
    to_encode = {"email": data, 'exp': expire}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY_EMAIL, algorithm=settings.ALGORITHM_EMAIL)
    return encoded_jwt


def decode_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY_EMAIL, algorithms=[settings.ALGORITHM_EMAIL])
        return payload
    except JWTError:
        raise errors.DecodeError("Error decoding token")
