from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_HOSTNAME: str
    DATABASE_PASSWORD: str
    DATABASE_USERNAME: str
    DATABASE_NAME: str
    DATABASE_PORT: int
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SMTP_SERVER: str
    SMTP_PORT: int
    EMAIL_ADDRESS: str
    PASSWORD_EMAIL: str
    SECRET_KEY_EMAIL: str
    ALGORITHM_EMAIL: str

    class Config:
        env_file = ".env"


settings = Settings()
