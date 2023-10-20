from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

from app.models.models import Base

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'


engine = create_engine(SQLALCHEMY_DATABASE_URL)


Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
