from pydantic import ConfigDict, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = "postgresql+asyncpg://postgres:goitserhii@localhost:5432/group_project"
    SECRET_KEY_JWT: str = ""
    ALGORITHM: str = "HS256"
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = "postgres@localhost"
    MAIL_PORT: int = 5432
    MAIL_SERVER: str = "localhost"

    @field_validator("ALGORITHM")
    @classmethod
    def validate_algorithm(cls, v):
        """
        Validate the provided JWT algorithm.

        Args:
        - v (str): The algorithm to validate.

        Raises:
        - ValueError: If the provided algorithm is not supported.

        Returns:
        - str: The validated algorithm.
        """
        if v not in ["HS256", "HS512"]:
            raise ValueError("Algorithm not supported")
        return v

    model_config = ConfigDict(extra="ignore", env_file=".env", env_file_encoding="utf-8")  # noqa


config = Settings()
