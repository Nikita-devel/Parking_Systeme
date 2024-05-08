from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.responses import JSONResponse

from src.database.db import get_db
from src.database.models import User, Role
from src.schemas.user import UserResponse
from src.services.auth import auth_service
from src.conf.config import config
from src.repository import users as repositories_users

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user(user: User = Depends(auth_service.get_current_user)):
    return user


@router.post("/assign-moderator-role/{user_id}", response_model=UserResponse)
async def assign_moderator_role(username: str, db: AsyncSession = Depends(get_db),
                                current_user: User = Depends(auth_service.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")

    user = await repositories_users.get_user_by_username(username, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = Role.admin
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/remove-moderator-role/{user_id}", response_model=UserResponse)
async def remove_moderator_role(user_id: int, db: AsyncSession = Depends(get_db),
                                current_user: User = Depends(auth_service.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")

    user = await repositories_users.get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = Role.user
    await db.commit()
    await db.refresh(user)
    return user


async def set_admin_role(email: str, db: AsyncSession = Depends(get_db)):
    user = await repositories_users.get_user_by_email(email, db)
    if user:
        user.role = Role.admin
        await db.commit()
        await db.refresh(user)
        return {"message": f"User with email {email} now has admin role"}
    else:
        raise HTTPException(status_code=404, detail="User not found")
