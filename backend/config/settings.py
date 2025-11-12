# backend/config/settings.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_USER: str
    MONGO_PASS: str
    MONGO_HOST: str
    MONGO_PORT: int
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

    class Config:
        env_file = ".env"


settings = Settings()
