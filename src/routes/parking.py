from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.responses import JSONResponse

from src.database.db import get_db
from src.database.models import User, Role
from src.schemas.parking import ParkingRateSchema
from src.services.auth import auth_service
from src.conf.config import config
from src.repository import users as repositories_users
from src.repository import parking as repositories_parking

router = APIRouter(prefix="/parking", tags=["parking"])


@router.post("/set-parking-rate", response_model=ParkingRateSchema)
async def set_parking_rate(rate: int, db: AsyncSession = Depends(get_db),
                           current_user: User = Depends(auth_service.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")
    else:
        if rate >= 0:
            rate_return = await repositories_parking.set_parking_rate(rate, db)
            return rate_return.rate

        else:
            raise HTTPException(status_code=400,
                                detail="Недопустимая стоимость. Стоимость должна быть неотрицательной.")
