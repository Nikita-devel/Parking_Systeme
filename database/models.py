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
    """
    Enumeration representing user roles.

    Attributes:
    - admin (str): Administrator role.
    - moderator (str): Moderator role.
    - user (str): User role.
    """
    admin: str = "admin"
    moderator: str = "moderator"
    user: str = "user"


class User(Base):
    """
    SQLAlchemy model representing user information.

    Attributes:
    - id (int): User ID (primary key).
    - username (str): User's username.
    - email (str): User's email (unique).
    - password (str): User's password.
    - avatar (str): URL of the user's avatar.
    - refresh_token (str): Refresh token for authentication.
    - created_at (date): Date of user creation.
    - updated_at (date): Date of last user update.
    - role (Enum): User's role (admin, moderator, user).
    - confirmed (bool): Flag indicating if the user's email is confirmed.

    Properties:
    - is_admin (bool): Property indicating if the user has an admin role.
    - is_moderator (bool): Property indicating if the user has a moderator role.
    """
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[date] = mapped_column("created_at", DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column("updated_at", DateTime, default=func.now(), onupdate=func.now())
    role: Mapped[Enum] = mapped_column("role", Enum(Role), default=Role.user, nullable=True)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)

    @property
    def is_admin(self):
        """
        Check if the user has an admin role.

        Returns:
        - bool: True if the user has an admin role, False otherwise.
        """
        return self.role == Role.admin

    @property
    def is_moderator(self):
        """
        Check if the user has a moderator role.

        Returns:
        - bool: True if the user has a moderator role, False otherwise.
        """
        return self.role == Role.moderator