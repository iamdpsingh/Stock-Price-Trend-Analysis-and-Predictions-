from pydantic_settings import BaseSettings
from pydantic import Field, AnyUrl

class Settings(BaseSettings):
    MONGODB_URI: AnyUrl = Field(..., env="MONGODB_URI")
    MONGODB_DB_NAME: str = Field(..., env="MONGODB_DB_NAME")
    JWT_SECRET_KEY: str = Field(..., env="JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60*24, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    REDIS_URL: AnyUrl = Field(..., env="REDIS_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Ignore unknown environment variables

settings = Settings()
