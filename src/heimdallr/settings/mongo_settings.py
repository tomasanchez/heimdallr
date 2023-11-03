"""Mongo Settings module.

Defines environment variables configuration
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class MongoSettings(BaseSettings):
    """Define application configuration model.

    Constructor will attempt to determine the values of any fields not passed
    as keyword arguments by reading from the environment. Default values will
    still be used if the matching environment variable is not set.

    Environment variables:
        * MONGO_CLIENT
        * MONGO_USER
        * MONGO_PASSWORD

    Attributes:
        CLIENT (str): MongoDB client url.
        USER (str): MongoDB user.
        PASSWORD (str): MongoDB password.
    """

    CLIENT: str = "mongodb://localhost:27017"
    DATABASE: str = "heimdallr-dev"
    USER: str | None = None
    PASSWORD: str | None = None

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_prefix="MONGO_",
    )
