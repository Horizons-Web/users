from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
import sentry_sdk

from fastapi_mail import ConnectionConfig

import os


def configure_cors(app: FastAPI):
    origins = [
        "http://localhost:8080",
    ]
    app.add_middleware(
        CORSMiddleware,
        #allow_origins=origins,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def configure_sentry(app: FastAPI):
    sentry_sdk.init(
        dsn=Settings.DSN_SENTRY,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )
    app.add_middleware(SentryAsgiMiddleware)


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

    DSN_SENTRY = os.getenv("DSN_SENTRY")

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
