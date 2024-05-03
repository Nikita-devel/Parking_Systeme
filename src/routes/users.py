import cloudinary
import cloudinary.uploader
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
cloudinary.config(cloud_name=config.CLD_NAME, api_key=config.CLD_API_KEY, api_secret=config.CLD_API_SECRET, secure=True)


@router.get("/me", response_model=UserResponse)
async def get_current_user(user: User = Depends(auth_service.get_current_user)):
    """
    Endpoint to get information about the currently authenticated user.

    Args:
    - user (User): Current authenticated user.

    Returns:
    - UserResponse: User information response.
    """
    return user


@router.patch("/avatar", response_model=UserResponse)
async def update_avatar(
    file: UploadFile = File(),
    user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Endpoint to update user avatar.

    Args:
    - file (UploadFile): Avatar file to upload.
    - user (User): Current authenticated user.
    - db (AsyncSession): Async database session.

    Returns:
    - UserResponse: Updated user information response.
    """
    public_id = f"Web16/{user.email}"
    res = cloudinary.uploader.upload(file.file, public_id=public_id, owerite=True)
    res_url = cloudinary.CloudinaryImage(public_id).build_url(
        width=250, height=250, crop="fill", version=res.get("version")
    )
    user = await repositories_users.update_avatar(user.email, res_url, db)
    # auth_service.cache.set(user.email, pickle.dumps(user))
    # auth_service.cache.expire(user.email, 300)
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


@router.post("/assign-moderator-role/{user_id}", response_model=UserResponse)
async def assign_moderator_role(user_id: int, db: AsyncSession = Depends(get_db),
                                current_user: User = Depends(auth_service.get_current_user)):
    """
    Endpoint to assign the moderator role to a user.

    Args:
    - user_id (int): User ID to assign the moderator role.
    - db (AsyncSession): Async database session.
    - current_user (User): Current authenticated user.

    Returns:
    - UserResponse: Updated user information response.

    Raises:
    - HTTPException: If the current user is not an admin or the user to be modified is not found.
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")

    user = await repositories_users.get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = Role.moderator
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/remove-moderator-role/{user_id}", response_model=UserResponse)
async def remove_moderator_role(user_id: int, db: AsyncSession = Depends(get_db),
                                current_user: User = Depends(auth_service.get_current_user)):
    """
    Endpoint to remove the moderator role from a user.

    Args:
    - user_id (int): User ID to remove the moderator role.
    - db (AsyncSession): Async database session.
    - current_user (User): Current authenticated user.

    Returns:
    - UserResponse: Updated user information response.

    Raises:
    - HTTPException: If the current user is not an admin or the user to be modified is not found.
    """
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
    """
    Endpoint to set the admin role for a user.

    Args:
    - email (str): Email of the user to set the admin role.
    - db (AsyncSession): Async database session.

    Returns:
    - dict: Response message.

    Raises:
    - HTTPException: If the user is not found.
    """
    user = await repositories_users.get_user_by_email(email, db)
    if user:
        user.role = Role.admin
        await db.commit()
        await db.refresh(user)
        return {"message": f"User with email {email} now has admin role"}
    else:
        raise HTTPException(status_code=404, detail="User not found")
