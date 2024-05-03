from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from libgravatar import Gravatar

from src.database.db import get_db
from src.database.models import User, Role
from src.schemas.user import UserSchema


async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    """
        Retrieve a user by email.

        Args:
            email (str): The email address of the user.
            db (AsyncSession, optional): The asynchronous database session. Defaults to Depends(get_db).

        Returns:
            User: The retrieved user, or None if not found.
        """
    stmt = select(User).filter_by(email=email)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    return user

async def get_user_by_username(username: str, db: AsyncSession = Depends(get_db)):
    """
        Retrieve a user by username.

        Args:
            username (str): The username of the user.
            db (AsyncSession, optional): The asynchronous database session. Defaults to Depends(get_db).

        Returns:
            User: The retrieved user, or None if not found.
        """
    stmt = select(User).filter_by(username=username)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    return user

async def create_user(body: UserSchema, db: AsyncSession = Depends(get_db)):
    """
        Create a new user.

        Args:
            body (UserSchema): The user data.
            db (AsyncSession, optional): The asynchronous database session. Defaults to Depends(get_db).

        Returns:
            User: The created user.
        """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as err:
        print(err)

    new_user = User(**body.model_dump(), avatar=avatar)

    stmt = select(User).limit(1)
    existing_user = (await db.execute(stmt)).first()

    if not existing_user:
        new_user.role = Role.admin

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: AsyncSession):
    """
        Update the refresh token of a user.

        Args:
            user (User): The user.
            token (str, optional): The new refresh token.
            db (AsyncSession): The asynchronous database session.
        """
    user.refresh_token = token
    await db.commit()

async def confirmed_email(email: str, db: AsyncSession):
    """
        Confirm the email address of a user.

        Args:
            email (str): The email address of the user.
            db (AsyncSession): The asynchronous database session.
        """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()

async def update_avatar(email, url: str, db: AsyncSession) -> User:
    """
        Update the avatar URL of a user.

        Args:
            email: The email address of the user.
            url (str): The new avatar URL.
            db (AsyncSession): The asynchronous database session.

        Returns:
            User: The updated user.
        """
    user = await get_user_by_email(email, db)
    user.avatar = url
    await db.commit()
    await db.refresh(user)
    return user

async def get_all_users(db: AsyncSession = Depends(get_db)):
    """
        Retrieve all users.

        Args:
            db (AsyncSession, optional): The asynchronous database session. Defaults to Depends(get_db).

        Returns:
            List[User]: The list of users.
        """
    stmt = select(User)
    users = await db.execute(stmt)
    return users.scalars().all()


async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    """
        Retrieve a user by ID.

        Args:
            user_id (int): The ID of the user.
            db (AsyncSession, optional): The asynchronous database session. Defaults to Depends(get_db).

        Returns:
            User: The retrieved user, or None if not found.
        """
    stmt = select(User).filter_by(id=user_id)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    return user
