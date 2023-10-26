from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


from app.config import settings

from app.models.models import Base

DATABASE_URI = os.getenv('DATABASE_URI_USERS')


engine = create_engine(DATABASE_URI)



Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
