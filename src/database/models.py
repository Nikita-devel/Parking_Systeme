import enum
from datetime import date
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, Integer, ForeignKey, DateTime, func, Enum, Boolean
# from pydantic import BaseModel



class Base(DeclarativeBase):
    """
    Base class for declarative SQLAlchemy models.
    """
    pass


class Role(enum.Enum):
    admin: str = "admin"
    user: str = "user"


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    role: Mapped[Enum] = mapped_column("role", Enum(Role), default=Role.user, nullable=True)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)

    balance = relationship("Balance", back_populates="user")
    plate = relationship("Plate", back_populates="user")

    @property
    def is_admin(self):
        return self.role == Role.admin


class Plate(Base):
    __tablename__ = "plates"
    id: Mapped[int] = mapped_column(primary_key=True)
    plate: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    black_mark: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)

    user: Mapped[relationship] = relationship("User", back_populates="plate")
    session = relationship("Session", back_populates="plate")


class Session(Base):
    __tablename__ = "sessions"
    id: Mapped[int] = mapped_column(primary_key=True)
    entrance_time: Mapped[date] = mapped_column(DateTime, default=func.now)
    exit_time: Mapped[date] = mapped_column(DateTime, nullable=True)
    plate_id: Mapped[int] = mapped_column(Integer, ForeignKey("plates.id"))
    total_hours_spent: Mapped[int] = mapped_column(Integer, nullable=True)
    total_coast: Mapped[int] = mapped_column(Integer, nullable=True)
    payment: Mapped[int] = mapped_column(Integer, default=0)

    plate: Mapped[relationship] = relationship("Plate", back_populates="session")


class Balance(Base):
    __tablename__ = "balance"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    total_balance: Mapped[int] = mapped_column(Integer, default=0)

    user: Mapped[relationship] = relationship("User", back_populates="balance")


class ParkingProperties(Base):
    __tablename__ = "parking_properties"
    id: Mapped[int] = mapped_column(primary_key=True)
    rate: Mapped[int] = mapped_column(Integer, default=0)
    space_amount: Mapped[int] = mapped_column(Integer, default=20)
    balance_limit: Mapped[int] = mapped_column(Integer, default=100)

