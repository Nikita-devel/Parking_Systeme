from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from src.database.db import get_db
from src.database.models import User, Role, ParkingProperties, Session, Plate
from src.schemas.user import UserSchema


async def entrance_for_authorized(plate: Plate, db: AsyncSession = Depends(get_db)):
    new_session = Session(entrance_time=datetime.now(), plate_id=plate.id)

    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    return new_session

