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


@router.post("/assign-admin-role/{email}", response_model=UserResponse)
async def assign_admin_role(email: str, db: AsyncSession = Depends(get_db),
                            current_user: User = Depends(auth_service.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")

    user = await repositories_users.get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = Role.admin
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/remove-admin-role/{username}", response_model=UserResponse)
async def remove_admin_role(username: str, db: AsyncSession = Depends(get_db),
                            current_user: User = Depends(auth_service.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")

    user = await repositories_users.get_user_by_username(username, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = Role.user
    await db.commit()
    await db.refresh(user)
    return user


@router.get("/all_users", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    """
    Endpoint to get a list of all users.
    Args:
    - db (AsyncSession): Async database session.
    - current_user (User): Current authenticated user.

    Returns:
    - List[UserResponse]: List of user information responses.

    Raises:
    - HTTPException: If the current user is not an admin.
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")
    users = await repositories_users.get_all_users(db)
    return users
