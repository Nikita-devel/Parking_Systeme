from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.responses import JSONResponse
from typing import Union

from src.database.db import get_db
from src.database.models import User, Role
from src.schemas.parking import ParkingRateSchema, ParkingBalanceLimitSchema, SessionInfoSchema, MessageResponse, \
    PlateSchema
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
            return ParkingRateSchema(rate=rate_return.rate)

        else:
            raise HTTPException(status_code=400,
                                detail="Недопустимая стоимость. Стоимость должна быть неотрицательной.")


@router.post("/set-balance-limit", response_model=ParkingBalanceLimitSchema)
async def set_balance_limit(balance_limit: int, db: AsyncSession = Depends(get_db),
                            current_user: User = Depends(auth_service.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")
    else:
        if balance_limit >= 0:
            balance_limit_return = await repositories_parking.set_balance_limit(balance_limit, db)
            return ParkingBalanceLimitSchema(balance_limit=balance_limit_return.balance_limit)

        else:
            raise HTTPException(status_code=400,
                                detail="Недопустимая стоимость. Стоимость должна быть неотрицательной.")


@router.get("/search_plate/{plate}", response_model=Union[list[SessionInfoSchema], MessageResponse])
async def searching_plate(plate: str, db: AsyncSession = Depends(get_db),
                          current_user: User = Depends(auth_service.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")
    else:
        plate_info = await repositories_parking.search_plate(plate, db)
        if plate_info:
            plate_sessions = await repositories_parking.get_sessions_for_plate(plate_info.id, db)

            if plate_sessions:
                return plate_sessions

            else:
                return MessageResponse(message=" This plate hasn't sessions")

        else:
            return MessageResponse(message="Plate is not registered")


@router.post("/add_new_plate/{plate}", response_model=PlateSchema)
async def add_new_plate(plate: str, db: AsyncSession = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")

    else:
        new_plate_to_bd = await repositories_parking.adding_new_plate(plate, db=db)

        if new_plate_to_bd is None:
            raise HTTPException(status_code=409, detail="This plate is already registered")

        return PlateSchema(id=new_plate_to_bd.id, plate=new_plate_to_bd.plate, user_id=new_plate_to_bd.user_id)


@router.post("/remove_plate/{plate}", response_model=MessageResponse)
async def remove_plate(plate: str, db: AsyncSession = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")

    else:
        result_delete_plate = await repositories_parking.delete_plate(plate, db)
        return MessageResponse(message=result_delete_plate)

