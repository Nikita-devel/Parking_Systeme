from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.responses import JSONResponse
from typing import Union, Optional

from src.database.db import get_db
from src.database.models import User, Role
from src.schemas.parking import ParkingRateSchema, ParkingBalanceLimitSchema, SessionInfoSchema, MessageResponse, \
    PlateSchema
from src.services.auth import auth_service
from src.conf.config import config
from src.repository import users as repositories_users
from src.repository import parking as repositories_parking
from src.repository import parking_services as repositories_parking_services

router = APIRouter(prefix="/parking_services", tags=["parking services"])


@router.post("/entrance", response_model=SessionInfoSchema)
async def entrance(plate: str, db: AsyncSession = Depends(get_db),
                   current_user: Optional[User] = Depends(auth_service.get_current_user)):
    check_plate = await repositories_parking.search_plate(plate, db)
    if check_plate is None:
        check_plate = await repositories_parking.adding_new_plate(plate, current_user.id, db)

    new_session = await repositories_parking_services.entrance_for_authorized(check_plate, db)
    return SessionInfoSchema(entrance_time=new_session.entrance_time, exit_time=new_session.exit_time,
                             total_hours_spent=new_session.total_hours_spent, total_coast=new_session.total_coast,
                             payment=new_session.payment)
