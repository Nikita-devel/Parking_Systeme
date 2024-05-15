from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from src.database.db import get_db
from src.database.models import User, Role, ParkingProperties, Session, Plate
from src.schemas.user import UserSchema


async def entrance_for_authorized(plate: Plate, db: AsyncSession = Depends(get_db)):
    check_session = await db.execute(
        select(Session).where(Session.plate_id == plate.id, Session.exit_time.is_(None))
    )
    open_sessions = check_session.scalars().all()

    if len(open_sessions) > 0:
        return "We have an open session already"

    new_session = Session(entrance_time=datetime.now(), plate_id=plate.id)
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    return new_session

async def exit(plate: Plate, db: AsyncSession = Depends(get_db)):
    check_session = await db.execute(select(Session).filter_by(plate_id=plate.id, exit_time=None))

    check_session = check_session.scalar_one_or_none()

    if check_session is None:
        return "No such session exists"
    else:
        check_session.exit_time = datetime.now()
        rate = await db.execute(select(ParkingProperties.rate))
        rate = rate.scalar()
        time = (datetime.now() - check_session.entrance_time).total_seconds() // 3600
        if time < 1:
            time = 1
        check_session.total_hours_spent = time
        check_session.total_coast = time * rate
        check_session.payment = time * rate

        await db.commit()
        await db.refresh(check_session)
        return check_session