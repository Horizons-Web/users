from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True, index=True)
    lat = Column(Float)
    lng = Column(Float)
    country = Column(String, nullable=False)
    administrative_area_level_1 = Column(String, nullable=False)
    administrative_area_level_2 = Column(String)
    locality = Column(String, nullable=False)
    postal_code = Column(String)
    street = Column(String)
    street_number = Column(String)
    place_id = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow, nullable=False)

    users = relationship("Users", back_populates="address")


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)
    user_type = Column(String, nullable=False)

    address_id = Column(Integer, ForeignKey('address.id'))
    address = relationship("Address", back_populates="users")
    client = relationship("Client", back_populates="users")
    token = relationship("Token", back_populates="users")


class Client(Base):
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True, index=True)
    dni = Column(String, unique=True, index=True)
    physical_level = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    users = relationship("Users", back_populates="client")


class Token(Base):
    __tablename__ = 'token'

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, nullable=False, unique=True)
    role = Column(String, nullable=False)
    expiration_date = Column(DateTime, default=datetime.utcnow(), nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)

    users = relationship("Users", back_populates="token")
