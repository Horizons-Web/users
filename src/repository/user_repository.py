from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from contextlib import contextmanager

from src.db_config import database
from src.models import models
from src.schema import user_schema, token_schema
from src.utils import errors


def _add_tables():
    return models.Base.metadata.create_all(bind=database.engine)


class UserRepository:
    @staticmethod
    @contextmanager
    def get_db() -> Session:
        db = database.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    @staticmethod
    def create(user: user_schema.CreateRequest):
        with UserRepository.get_db() as db:
            try:
                new_user = models.Users(
                    username=user.username,
                    email=user.email,
                    password=user.password,
                    user_type=user.user_type,
                    is_active=False,
                )
                db.add(new_user)
                db.flush()
                if user.user_type == 'guide':
                    guide = models.Guide(
                        user_id=new_user.id,
                    )
                    db.add(guide)
                if user.user_type == 'client':
                    client = models.Client(
                        user_id=new_user.id,
                    )
                    db.add(client)
                db.flush()
                db.commit()
                user_created = user_schema.CreateResponse(
                    id=new_user.id,
                    username=new_user.username,
                    email=new_user.email,
                    created_at=new_user.created_at,
                )
                return user_created
            except Exception as e:
                db.rollback()
                raise e

    @staticmethod
    def get(params: user_schema.Params):
        with UserRepository.get_db() as db:
            user = None
            if params.id:
                user = db.query(models.Users).filter(models.Users.id == params.id).first()
            elif params.username:
                user = db.query(models.Users).filter(models.Users.username == params.username).first()
            elif params.email:
                user = db.query(models.Users).filter(models.Users.email == params.email).first()
            if user is None:
                raise errors.UserNotFound("User not found")
            user = user_schema.GetUser(
                id=str(user.id),
                username=user.username,
                email=user.email,
                password=user.password,
                user_type=user.user_type,
                is_active=user.is_active,
                address_id=str(user.address_id),
            )
            return user

    @staticmethod
    def put(params: user_schema.Params, user_update: user_schema.Update):
        print(user_update.dict())
        with UserRepository.get_db() as db:
            try:
                if params.id is not None:
                    user = db.query(models.Users).filter(models.Users.id == params.id).first()
                if params.username is not None:
                    user = db.query(models.Users).filter(models.Users.username == params.username).first()
                if params.email is not None:
                    user = db.query(models.Users).filter(models.Users.email == params.email).first()
                if user:
                    if user_update.username is not None:
                        user.username = user_update.username
                        db.flush()
                        db.commit()
                        return user.username
                    if user_update.email is not None:
                        user.email = user_update.email
                        db.flush()
                        db.commit()
                        return user.email
                    if user_update.password is not None:
                        user.password = user_update.password
                        db.flush()
                        db.commit()
                        return user.password
                    if user_update.is_active is not None:
                        user.is_active = user_update.is_active
                        db.flush()
                        db.commit()
                        return user.is_active
                else:
                    raise errors.UserNotFound("User not found")
            except SQLAlchemyError as e:
                db.rollback()
                raise errors.UpdateError("Error updating")


class TokenRepository:
    @staticmethod
    @contextmanager
    def get_db() -> Session:
        db = database.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    @staticmethod
    def get(params: token_schema.Params):
        with TokenRepository.get_db() as db:
            token = None
            if params.user_id is not None:
                token = db.query(models.Token).filter(models.Token.user_id == params.user_id).first()
            elif params.token is not None:
                token = db.query(models.Token).filter(models.Token.token == params.token).first()
            if token is None:
                if params.exists:
                    return None
                raise errors.TokenNotFound("Token not found")
            token = token_schema.Data(
                token=token.token,
                expiration_date=token.expiration_date,
                is_active=token.is_active,
                user_id=token.user_id,
                role=token.role,
            )
            return token

    @staticmethod
    def create(token_create: token_schema.Data):
        with TokenRepository.get_db() as db:
            try:
                new_token = models.Token(
                    token=token_create.token,
                    expiration_date=token_create.expiration_date,
                    is_active=token_create.is_active,
                    user_id=token_create.user_id,
                    role=token_create.role,

                )
                db.add(new_token)
                db.flush()
                db.commit()
                token_created = token_schema.Data(
                    token=new_token.token,
                    expiration_date=new_token.expiration_date,
                    is_active=new_token.is_active,
                    user_id=new_token.user_id,
                    role=new_token.role,
                )
                return token_created

            except Exception as e:
                db.rollback()
                raise e

    @staticmethod
    def update(token: token_schema.Data):
        with TokenRepository.get_db() as db:
            try:
                existing_token = db.query(models.Token).filter(models.Token.user_id == token.user_id).first()
                if existing_token:
                    if token.token is not None:
                        existing_token.token = token.token
                    if token.expiration_date is not None:
                        existing_token.expiration_date = token.expiration_date
                    if token.is_active is not None:
                        existing_token.is_active = token.is_active
                    if token.role is not None:
                        existing_token.role = token.role
                    db.flush()
                    db.commit()
                    token_updated = token_schema.Data(
                        token=existing_token.token,
                        expiration_date=existing_token.expiration_date,
                        is_active=existing_token.is_active,
                        user_id=existing_token.user_id,
                        role=existing_token.role,
                    )
                    return token_updated
                else:
                    raise errors.TokenNotFound("Token not found")

            except Exception as e:
                db.rollback()
                raise e