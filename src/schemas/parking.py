from pydantic import BaseModel, EmailStr, Field

from src.database.models import Role


class ParkingRateSchema(BaseModel):
    rate: int = Field(ge=1, le=500)


class ParkingBalanceLimitSchema(BaseModel):
    balance_limit: int = Field(ge=1, le=5000)