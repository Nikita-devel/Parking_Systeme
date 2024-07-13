from pydantic import ConfigDict, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = "postgresql+asyncpg://postgres:02012009@localhost:5432/postgres"
    SECRET_KEY_JWT: str = "974790aec4ac460bdc11645decad4dce7c139b7f2982b7428ec44e886ea588c6"
    ALGORITHM: str = "HS256"
    MAIL_USERNAME: str = "mail_username"
    MAIL_PASSWORD: str = "mail_password"
    MAIL_FROM: str = "mail_from"
    MAIL_PORT: int = 465
    MAIL_SERVER: str = "mail_server"

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
