from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.database.models import User, Role, ParkingProperties, Session, Plate
from src.schemas.user import UserSchema


async def get_parking_properties(db: AsyncSession = Depends(get_db)):
    stmt = select(ParkingProperties)
    parking_properties = await db.execute(stmt)
    parking_properties = parking_properties.scalar_one_or_none()

    if parking_properties is None:
        return None

    return parking_properties


async def set_parking_rate(new_rate: int, db: AsyncSession = Depends(get_db)):
    stmt = select(ParkingProperties)
    rate = await db.execute(stmt)
    rate = rate.scalar_one_or_none()

    if rate is None:
        create_rate = ParkingProperties(rate=new_rate)
        db.add(create_rate)
        await db.commit()
        await db.refresh(create_rate)
        return create_rate
    else:
        rate.rate = new_rate
        await db.commit()
        await db.refresh(rate)
        return rate


async def set_balance_limit(new_balance_limit: int, db: AsyncSession = Depends(get_db)):
    stmt = select(ParkingProperties)
    parking_properties = await db.execute(stmt)
    parking_properties = parking_properties.scalar_one_or_none()

    if parking_properties is None:
        create_balance_limit = ParkingProperties(balance_limit=new_balance_limit)
        db.add(create_balance_limit)
        await db.commit()
        await db.refresh(create_balance_limit)
        return create_balance_limit
    else:
        parking_properties.balance_limit = new_balance_limit
        await db.commit()
        await db.refresh(parking_properties)
        return parking_properties


async def get_sessions_for_plate(plate_id: int, db: AsyncSession = Depends(get_db())):
    stmt = select(Session).filter_by(plate_id=plate_id)
    plate_sessions = await db.execute(stmt)
    plate_sessions = plate_sessions.scalars().all()

    if plate_sessions:
        return plate_sessions

    else:
        return None


async def search_plate(plate: str, db: AsyncSession = Depends(get_db())):
    stmt = select(Plate).filter_by(plate=plate)
    plate_info = await db.execute(stmt)
    plate_info = plate_info.scalar_one_or_none()

    return plate_info


async def adding_new_plate(plate: str, user_id: int = None, db: AsyncSession = Depends(get_db())):
    new_plate = Plate(plate=plate, user_id=user_id)

    stmt = select(Plate).filter_by(plate=plate)
    check_plate = await db.execute(stmt)
    check_plate = check_plate.scalar_one_or_none()

    if check_plate is None:
        db.add(new_plate)
        await db.commit()
        await db.refresh(new_plate)
        return new_plate
    else:
        return None


async def delete_plate(plate: str, db: AsyncSession = Depends(get_db())):
    stmt = select(Plate).filter_by(plate=plate)
    check_plate = await db.execute(stmt)
    check_plate = check_plate.scalar_one_or_none()

    if check_plate is None:
        return f"{plate} номера нет в БД"

    elif check_plate.user_id is not None:
        return "Вы не можете удалить номер зарегистрированного пользователя"

    else:
        await db.delete(check_plate)
        await db.commit()
        return f"Номер {plate} был успешно удален"