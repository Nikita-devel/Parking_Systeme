import cv2
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
from src.neural_network.neural_net import get_num_avto

router = APIRouter(prefix="/parking_services", tags=["parking services"])


@router.post("/entrance", response_model=Union[SessionInfoSchema, MessageResponse])
async def entrance(file: UploadFile = File(...), db: AsyncSession = Depends(get_db),
                   current_user: Optional[User] = Depends(auth_service.get_current_user)):
    contents = await file.read()
    with open(f"./img/{file.filename}", "wb") as f:
        f.write(contents)

    # Завантаження зображення
    original = cv2.imread(f"./img/{file.filename}")

    # Розпізнавання номерного знаку
    plate_number, _ = get_num_avto(original)
    check_plate = await repositories_parking.search_plate(plate_number, db)
    if check_plate is None:
        check_plate = await repositories_parking.adding_new_plate(plate_number, current_user.id, db)

    new_session = await repositories_parking_services.entrance_for_authorized(check_plate, db)

    if type(new_session) == str:
        return MessageResponse(message=new_session)
    else:
        return SessionInfoSchema(entrance_time=new_session.entrance_time, exit_time=new_session.exit_time,
                                total_hours_spent=new_session.total_hours_spent, total_coast=new_session.total_coast,
                                payment=new_session.payment)

@router.post("/exit", response_model=Union[SessionInfoSchema, MessageResponse])
async def exit(file: UploadFile = File(...), db: AsyncSession = Depends(get_db),
                   current_user: Optional[User] = Depends(auth_service.get_current_user)):
    contents = await file.read()
    with open(f"./img/{file.filename}", "wb") as f:
        f.write(contents)

    # Завантаження зображення
    original = cv2.imread(f"./img/{file.filename}")

    # Розпізнавання номерного знаку
    plate_number, _ = get_num_avto(original)
    check_plate = await repositories_parking.search_plate(plate_number, db)
    if check_plate is None:
        return MessageResponse(message="Check the license plate number")

    close_session = await repositories_parking_services.exit(check_plate, db)

    if type(close_session) == str:
        return MessageResponse(message=close_session)

    return SessionInfoSchema(entrance_time=close_session.entrance_time, exit_time=close_session.exit_time,
                             total_hours_spent=close_session.total_hours_spent, total_coast=close_session.total_coast,
                             payment=close_session.payment)