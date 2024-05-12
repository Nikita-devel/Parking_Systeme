from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from src.database.models import Role


class ParkingRateSchema(BaseModel):
    rate: int = Field(ge=1, le=500)


class ParkingBalanceLimitSchema(BaseModel):
    balance_limit: int = Field(ge=1, le=5000)


class SessionInfo(BaseModel):
    entrance_time: datetime = Field()
    exit_time: datetime = Field()
    owner: str = Field()
    total_hours_spent: int = Field()
    total_coast: int = Field()
    payment: int = Field()


class MessageResponse(BaseModel):
    message: str
