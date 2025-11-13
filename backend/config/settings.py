# backend/config/settings.py
from pydantic_settings import BaseSettings
from pydantic import computed_field


class Settings(BaseSettings):
    MONGO_USER: str
    MONGO_PASS: str
    MONGO_LOCAL_HOST: str
    MONGO_LOCAL_PORT: int
    MONGO_DOCKER_HOST: str
    MONGO_DB_NAME: str
    MINIO_ENDPOINT: str
    MINIO_USER: str
    MINIO_PASS: str
    MINIO_BUCKET: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_QUEUE_NAME: str
    GOOGLE_API_KEY: str
    BACKEND_API_URL: str

    @computed_field
    @property
    def MONGO_URI(self) -> str:
        """Construct the MongoDB URI for Docker networking."""
        return f"mongodb://{self.MONGO_USER}:{self.MONGO_PASS}@{self.MONGO_DOCKER_HOST}:27017/"

    class Config:
        env_file = ".env"


settings = Settings()
