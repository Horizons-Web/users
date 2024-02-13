import uuid

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID

from datetime import datetime

Base = declarative_base()


class TimeStampUUIDMixin:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)


class Address(Base, TimeStampUUIDMixin):
    __tablename__ = 'address'

    country = Column(String, nullable=False)
    administrative_area_level_1 = Column(String, nullable=False)
    administrative_area_level_2 = Column(String)
    locality = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    place_id = Column(String, unique=True)


class Users(Base, TimeStampUUIDMixin):
    __tablename__ = 'users'

    address_id = Column(UUID(as_uuid=True), ForeignKey('address.id'), nullable=True)
    client = relationship("Client", back_populates="users")
    guide = relationship("Guide", back_populates="users")
    token = relationship("Token", back_populates="users")

    username = Column(String, index=True, unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    user_type = Column(Enum('guide', 'client', 'admin', name='user_type'), nullable=False)


class Client(Base, TimeStampUUIDMixin):
    __tablename__ = 'client'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), unique=True)
    users = relationship("Users", back_populates="client")


class Guide(Base, TimeStampUUIDMixin):
    __tablename__ = 'guide'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), unique=True)
    users = relationship("Users", back_populates="guide")


class Token(Base, TimeStampUUIDMixin):
    __tablename__ = 'token'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    users = relationship("Users", back_populates="token")

    token = Column(String, nullable=False, unique=True)
    role = Column(Enum('guide', 'client', name='role', nullable=False))
    expiration_date = Column(DateTime, default=datetime.utcnow(), nullable=False)
