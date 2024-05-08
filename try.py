import enum
from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, Integer, ForeignKey, DateTime, func, Enum, Column, Boolean
from pydantic import BaseModel


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

    @property
    def is_admin(self):
        return self.role == Role.admin


class Plate(Base):
    __tablename__ = "plates"
    id: Mapped[int] = mapped_column(primary_key=True)
    plate: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="plates")


class Session(Base):
    __tablename__ = "sessions"
    id: Mapped[int] = mapped_column(primary_key=True)
    entrance_time: Mapped[date] = mapped_column(DateTime, default=func.now)
    exit_time: Mapped[date] = mapped_column(DateTime)
    plate_id: Mapped[int] = mapped_column(Integer, ForeignKey("plates.id"))
    total_hours_spent: Mapped[int] = mapped_column(Integer, default=0)
    total_coast: Mapped[int] = mapped_column(Integer, default=0)
    payment: Mapped[int] = mapped_column(Integer, default=0)

    plate = relationship("Plate", back_populates="sessions")


class Balance(Base):
    __tablename__ = "balance"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    total_balance: Mapped[int] = mapped_column(Integer, default=0)

    user = relationship("User", back_populates="balance")


class ParkingProperties(Base):
    __tablename__ = "parking_properties"
    id: Mapped[int] = mapped_column(primary_key=True)
    rate: Mapped[int] = mapped_column(Integer, default=0)
    space_amount: Mapped[int] = mapped_column(Integer, default=20)
    balance_limit: Mapped[int] = mapped_column(Integer, default=100)


User.balance = relationship("Balance", back_populates="users")
User.plate = relationship("Plate", back_populates="users")
Plate.session = relationship("Session", back_populates="plates")