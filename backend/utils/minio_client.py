# backend/utils/minio_client.py
from minio import Minio
from config.settings import settings

minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_USER,
    secret_key=settings.MINIO_PASS,
    secure=False,
)


def initialize_minio_bucket():
    """Checks if the bucket exists and creates it if it does not."""
    try:
        bucket_name = settings.MINIO_BUCKET
        found = minio_client.bucket_exists(bucket_name)
        if not found:
            minio_client.make_bucket(bucket_name)
            print(f"Bucket '{bucket_name}' created successfully.")
        else:
            print(f"Bucket '{bucket_name}' already exists.")
    except Exception as e:
        print(f"Error initializing Minio bucket: {e}")
