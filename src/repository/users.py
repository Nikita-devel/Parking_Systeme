from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.database.models import User, Role
from src.schemas.user import UserSchema


async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    stmt = select(User).filter_by(email=email)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    return user


async def get_user_by_username(username: str, db: AsyncSession = Depends(get_db)):
    stmt = select(User).filter_by(username=username)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    return user


async def create_user(body: UserSchema, db: AsyncSession = Depends(get_db)):
    new_user = User(**body.model_dump())

    stmt = select(User).limit(1)
    existing_user = (await db.execute(stmt)).first()

    if not existing_user:
        new_user.role = Role.admin

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: AsyncSession):
    user.refresh_token = token
    await db.commit()


async def confirmed_email(email: str, db: AsyncSession):
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()


async def get_all_users(db: AsyncSession = Depends(get_db)):
    stmt = select(User)
    users = await db.execute(stmt)
    return users.scalars().all()


# async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
#     stmt = select(User).filter_by(id=user_id)
#     user = await db.execute(stmt)
#     user = user.scalar_one_or_none()
#     return user
