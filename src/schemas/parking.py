from pydantic import BaseModel, EmailStr, Field

from src.database.models import Role


class ParkingRateSchema(BaseModel):
    """
    Pydantic model for creating a new user.
    """
    rate: int = Field(min_length=1, max_length=50)
