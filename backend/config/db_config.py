# backend/config/db_config.py
import logging
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from bson import ObjectId
import datetime
from .settings import settings

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages the connection to MongoDB and provides access to collections."""

    _client: MongoClient = None
    _db: Database = None

    def connect(self):
        """Establishes the connection to the database."""
        if self._client is None:
            try:
                self._client = MongoClient(
                    settings.MONGO_URI, serverSelectionTimeoutMS=5000
                )
                self._client.admin.command("ismaster")
                self._db = self._client[settings.MONGO_DB_NAME]
                logger.info("Successfully connected to MongoDB.")
            except Exception as e:
                logger.error(f"Failed to connect to MongoDB: {e}")
                raise

    def close(self):
        """Closes the database connection."""
        if self._client:
            self._client.close()
            logger.info("MongoDB connection closed.")

    def get_calls_collection(self) -> Collection:
        """Returns the 'calls' collection instance."""
        if self._db is None:
            self.connect()
        return self._db["calls"]


db_manager = DatabaseManager()


# --- CRUD Functions using the manager ---
def create_call_record(original_filename: str, minio_path: str) -> str:
    calls_collection = db_manager.get_calls_collection()
    doc = {
        "original_filename": original_filename,
        "minio_path": minio_path,
        "upload_timestamp": datetime.datetime.now(datetime.timezone.utc),
        "status": "PENDING",  # Statuses: PENDING -> PROCESSING -> TRANSCRIBED -> ANALYZED (when all the langchain is done) ->  COMPLETED  (when ner is done) -> FAILED
        "analysis_results": None,
        "processing_error": None,
    }
    result = calls_collection.insert_one(doc)
    logger.info(
        f"Created MongoDB record for '{original_filename}' with ID: {result.inserted_id}"
    )
    return str(result.inserted_id)


def get_call_by_id(call_id: str) -> dict | None:
    """Fetches a call document by its ID."""
    calls_collection = db_manager.get_calls_collection()
    return calls_collection.find_one({"_id": ObjectId(call_id)})


def update_call_status(call_id: str, status: str, error_message: str | None = None):
    """Updates the status and optional error message of a call."""
    calls_collection = db_manager.get_calls_collection()
    update_doc = {"$set": {"status": status}}
    if error_message:
        update_doc["$set"]["processing_error"] = error_message
    calls_collection.update_one({"_id": ObjectId(call_id)}, update_doc)


def save_analysis_results(call_id: str, results: dict):
    """Saves the full analysis results and updates the status to COMPLETED."""
    calls_collection = db_manager.get_calls_collection()
    calls_collection.update_one(
        {"_id": ObjectId(call_id)},
        {"$set": {"analysis_results": results, "status": "COMPLETED"}},
    )
