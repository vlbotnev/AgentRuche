# backend/utils/minio_client.py
import logging
from minio import Minio
from config.settings import settings
import io

logger = logging.getLogger(__name__)


class MinioManager:
    """Manages the connection to Minio."""

    _client: Minio = None

    def connect(self):
        """Initializes the Minio client."""
        if self._client is None:
            try:
                self._client = Minio(
                    settings.MINIO_ENDPOINT,
                    access_key=settings.MINIO_USER,
                    secret_key=settings.MINIO_PASS,
                    secure=False,
                )
                logger.info("Minio client initialized.")
            except Exception as e:
                logger.error(f"Failed to initialize Minio client: {e}")
                raise

    def get_client(self) -> Minio:
        """Returns the Minio client instance."""
        if self._client is None:
            self.connect()
        return self._client


minio_manager = MinioManager()


def initialize_minio_bucket():
    """Checks if the bucket exists and creates it if it does not."""
    client = minio_manager.get_client()
    try:
        bucket_name = settings.MINIO_BUCKET
        found = client.bucket_exists(bucket_name)
        if not found:
            client.make_bucket(bucket_name)
            logger.info(f"Bucket '{bucket_name}' created successfully.")
        else:
            logger.info(f"Bucket '{bucket_name}' already exists.")
    except Exception as e:
        logger.error(f"Error initializing Minio bucket: {e}")


def upload_file_to_minio(file_name: str, file_data: io.BytesIO, file_size: int) -> str:
    """Uploads a file-like object to Minio and returns the object name."""
    client = minio_manager.get_client()
    bucket_name = settings.MINIO_BUCKET
    try:
        client.put_object(
            bucket_name=bucket_name,
            object_name=file_name,
            data=file_data,
            length=file_size,
        )
        logger.info(
            f"Successfully uploaded {file_name} to Minio bucket '{bucket_name}'."
        )
        return file_name
    except Exception as e:
        logger.error(f"Error uploading to Minio: {e}")
        raise
