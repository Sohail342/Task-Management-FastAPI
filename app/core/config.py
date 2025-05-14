from pydantic import Field
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Task Management System"
    DEBUG: bool = True


    # Database settings
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    
    # JWT Auth
    AUTHJWT_SECRET_KEY: str = Field(..., env="AUTHJWT_SECRET_KEY")
    AUTHJWT_ALGORITHM: str = Field("HS256", env="AUTHJWT_ALGORITHM")
    AUTHJWT_ACCESS_TOKEN_EXPIRES: int = Field(3600, env="AUTHJWT_ACCESS_TOKEN_EXPIRES")
    AUTHJWT_REFRESH_TOKEN_EXPIRES: int = Field(86400, env="AUTHJWT_REFRESH_TOKEN_EXPIRES")


    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache(maxsize=32)
def get_settings() -> Settings:
    """
    Get the application settings.

    Returns:
        Settings: The application settings.
    """
    return Settings()