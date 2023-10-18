from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from ..config import settings

DATABASE_URL = (
    f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@localhost/{settings.DATABASE_NAME}'
)

engine = create_engine(DATABASE_URL)

Base = declarative_base()

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
