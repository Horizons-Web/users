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
    #DATABASE_USER = "joaquin"
    #DATABASE_NAME = "users-db"
    #DATABASE_PASSWORD = "rootroot"
    #DATABASE_UNIX_SOCKET_PATH = "/cloudsql/crested-primacy-413823:us-central1:users"
    #SECRET_KEY = os.getenv("SECRET_KEY")
    #ALGORITHM = os.getenv("ALGORITHM")
    #ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    SMTP_SERVER = "indanet2.ferozo.com"
    SMTP_PORT = int(465)
    EMAIL_ADDRESS = "joaquinreyero@globaltechsrl.com.ar"
    PASSWORD_EMAIL = "Gurumiguel@2023"
    #SECRET_KEY_EMAIL = os.getenv("SECRET_KEY_EMAIL")
    #ALGORITHM_EMAIL = os.getenv("ALGORITHM_EMAIL")
    DATABASE_URI = "postgresql://joaquin:rootroot@/users-dev?host=/cloudsql/crested-primacy-413823:us-central1:users"
    #USERS_LOCALHOST = os.getenv("USERS_LOCALHOST")
    DSN_SENTRY = "https://31ca75b4272c073024fbd9ee92fc5173@o4506679202283520.ingest.sentry.io/4506694083674112"
    TEST = os.getenv("test")
    print(TEST)
    
settings = Settings()
