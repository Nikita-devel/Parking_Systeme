from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.database.models import User, Role, ParkingProperties
from src.schemas.user import UserSchema


async def get_parking_properties(db: AsyncSession = Depends(get_db)):
    stmt = select(ParkingProperties)
    parking_properties = await db.execute(stmt)
    parking_properties = parking_properties.first()
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
