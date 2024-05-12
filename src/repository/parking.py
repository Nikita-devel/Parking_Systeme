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
    rate = rate.first()

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
