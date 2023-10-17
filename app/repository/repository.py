from typing import TYPE_CHECKING
from sqlalchemy.orm import Session
from datetime import datetime

from ..db_config import database
from ..models import models
from ..schema import schema

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def _add_tables():
    return models.Base.metadata.create_all(bind=database.engine)


def get_db() -> Session:
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.Users).filter(models.Users.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.Users).filter(models.Users.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.Users).filter(models.Users.email == email).first()


def get_client_by_dni(db: Session, dni: str):
    return db.query(models.Users).filter(models.Client.dni == dni).first()


def get_password_by_username(db: Session, username: str):
    user = db.query(models.Users).filter(models.Users.username == username).first()
    if user:
        return user.password

    return None


def get_password_by_id(db: Session, user_id: int):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user:
        return user.password

    return None


def create_client(db: Session, client_create: schema.ClientCreate):

    address = models.Address(
        country=client_create.country,
        administrative_area_level_1=client_create.administrative_area_level_1,
        locality=client_create.locality,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(address)
    db.flush()

    user = models.Users(
        username=client_create.username,
        email=client_create.email,
        password=client_create.password,
        user_type="client",
        address_id=address.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(user)
    db.flush()

    client = models.Client(
        dni=client_create.dni,
        user_id=user.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(client)

    db.commit()

    response = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at,
    }

    return response


def deactivate_user(db: Session, user_id: int):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user:
        user.is_active = False
        user.updated_at = datetime.utcnow()
        db.commit()


def activate_user(db: Session, user_id: int):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user:
        user.is_active = True
        user.updated_at = datetime.utcnow()
        db.commit()


def change_password(db: Session, user_id: int, new_password: str):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not user:
        return None

    user.password = new_password
    user.updated_at = datetime.utcnow()

    db.commit()


