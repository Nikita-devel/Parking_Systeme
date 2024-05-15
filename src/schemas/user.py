from pydantic import BaseModel, EmailStr, Field

from src.database.models import Role


class UserSchema(BaseModel):
    """
    Pydantic model for creating a new user.
    """
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=8)


class UserResponse(BaseModel):
    """
    Pydantic model for the user response.
    """
    id: int = 1
    username: str
    email: EmailStr
    role: Role

    class Config:
        from_attributes = True


class TokenSchema(BaseModel):
    """
    Pydantic model for the token response.
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    """
    Pydantic model for requesting email.
    """
    email: EmailStr
