# backend/utils/redis_queue.py
import redis
import json
import logging
from config.settings import settings

logger = logging.getLogger(__name__)


class RedisManager:
    """Manages the connection to Redis."""

    _client: redis.Redis = None

    def connect(self):
        """Establishes the connection to Redis."""
        if self._client is None:
            try:
                self._client = redis.Redis(
                    host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    db=0,
                    decode_responses=True,  # Important for easier handling of data
                )
                self._client.ping()
                logger.info("Successfully connected to Redis.")
            except Exception as e:
                logger.error(f"Failed to connect to Redis: {e}")
                raise

    def close(self):
        """Closes the Redis connection."""
        if self._client:
            self._client.close()
            logger.info("Redis connection closed.")

    def get_client(self) -> redis.Redis:
        """Returns the Redis client instance."""
        if self._client is None:
            self.connect()
        return self._client


# Create a single instance
redis_manager = RedisManager()


# --- Queue Functions using the manager ---
def push_job_to_queue(job_data: dict):
    client = redis_manager.get_client()
    queue_name = settings.REDIS_QUEUE_NAME
    client.lpush(queue_name, json.dumps(job_data))
    logger.info(f"Pushed job {job_data} to queue '{queue_name}'.")


def get_job_from_queue() -> dict | None:
    client = redis_manager.get_client()
    queue_name = settings.REDIS_QUEUE_NAME
    _, job_json = client.brpop(queue_name, timeout=0)
    return json.loads(job_json)
