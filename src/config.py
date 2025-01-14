from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_mail import ConnectionConfig

import os


def configure_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def configure_mail():
    conf = ConnectionConfig(
        MAIL_USERNAME=settings.EMAIL_ADDRESS,
        MAIL_PASSWORD=settings.PASSWORD_EMAIL,
        MAIL_FROM=settings.EMAIL_ADDRESS,
        MAIL_PORT=settings.SMTP_PORT,
        MAIL_SERVER=settings.SMTP_SERVER,
        MAIL_STARTTLS=False,
        MAIL_SSL_TLS=True,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True
    )
    return conf


class Settings:

    if os.getenv("ENVIRONMENT") == "dev-local":
        DATABASE_URI = os.getenv("DATABASE_URI_LOCAL")
    else:
        DATABASE_URI = os.getenv("DATABASE_URI")

    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = int(os.getenv("SMTP_PORT"))
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    PASSWORD_EMAIL = os.getenv("PASSWORD_EMAIL")
    SECRET_KEY_EMAIL = os.getenv("SECRET_KEY_EMAIL")
    ALGORITHM_EMAIL = os.getenv("ALGORITHM_EMAIL")

    USERS_LOCALHOST = os.getenv("USERS_LOCALHOST")


settings = Settings()
