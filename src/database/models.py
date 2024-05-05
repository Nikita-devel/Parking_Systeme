from enum import Enum
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RoleEnum(str, Enum):
    admin = "admin"
    moderator = "moderator"
    user = "user"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    role = Column(String(50), default=RoleEnum.user, nullable=True)
    confirmed = Column(Boolean, default=False, nullable=True)


class Plate(Base):
    __tablename__ = "plates"
    id = Column(Integer, primary_key=True)
    plate = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="plates")


class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True)
    entrance_time = Column(DateTime, default=func.now)
    exit_time = Column(DateTime)
    plate_id = Column(Integer, ForeignKey("plates.id"))
    plate = relationship("Plate", back_populates="sessions")
    total_hours_spent = Column(Integer, default=0)


User.plates = relationship("Plate", back_populates="user")
Plate.sessions = relationship("Session", back_populates="plate")
