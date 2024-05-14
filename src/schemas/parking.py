from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from src.database.models import Role
from typing import Optional


class ParkingRateSchema(BaseModel):
    rate: int = Field(ge=1, le=500)


class ParkingBalanceLimitSchema(BaseModel):
    balance_limit: int = Field(ge=1, le=5000)


class SessionInfoSchema(BaseModel):
    entrance_time: datetime = Field()
    exit_time: Optional[datetime] = Field()
    total_hours_spent: Optional[int] = Field()
    total_coast: Optional[int] = Field()
    payment: int = Field()


class MessageResponse(BaseModel):
    message: str


class PlateSchema(BaseModel):
    id: int
    plate: str
    user_id: Optional[int]
    black_mark: bool
