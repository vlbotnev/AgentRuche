# backend/app.py
from fastapi import FastAPI, UploadFile, File
from contextlib import asynccontextmanager
from typing import List
from pydantic import BaseModel
import io
import logging
import uuid
import os

from config import db_config
from config.logging_config import setup_logging
from config.db_config import db_manager
from utils.redis_queue import redis_manager
from utils.minio_client import minio_manager
from utils import minio_client, redis_queue
# from tools import database_tools

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup...")
    setup_logging()
    db_manager.connect()
    redis_manager.connect()
    minio_manager.connect()
    yield
    db_manager.close()
    redis_manager.close()
    print("Application shutdown...")


app = FastAPI(title="AgentRouche API", lifespan=lifespan)


# --- Placeholder Routers (can be split into files later) ---
class ChatRequest(BaseModel):
    query: str


@app.post("/api/calls/upload")
async def upload_calls(files: List[UploadFile] = File(...)):
    """Handles uploading of one or more audio files."""
    call_ids = []
    for file in files:
        try:
            file_extension = os.path.splitext(file.filename)[1]
            file_name = os.path.splitext(file.filename)[0]
            unique_filename = f"{file_name}_{uuid.uuid4()}{file_extension}"

            # Read file content into memory
            file_content = file.file.read()
            file_size = len(file_content)
            file_stream = io.BytesIO(file_content)

            # 1. Save to Minio
            minio_path = minio_client.upload_file_to_minio(
                file_name=unique_filename, file_data=file_stream, file_size=file_size
            )

            # 2. Create DB record
            call_id = db_config.create_call_record(
                original_filename=file.filename,
                minio_path=minio_path,
            )

            # 3. Push job to Redis queue
            redis_queue.push_job_to_queue({"call_id": call_id})

            call_ids.append(call_id)
        except Exception as e:
            logger.error(f"Failed to process file {file.filename}: {e}", exc_info=True)
            # Handle potential failures during the upload process
            return {"error": f"Failed to process file {file.filename}: {e}"}

    return {"message": "Files queued for processing.", "call_ids": call_ids}


@app.get("/api/calls")
async def get_all_calls():
    print("Placeholder: /api/calls hit")
    return [{"id": "1", "filename": "call1.wav"}]


@app.get("/api/calls/{call_id}")
async def get_call_details(call_id: str):
    print(f"Placeholder: /api/calls/{call_id} hit")
    return {"id": call_id, "detail": "some mock data"}


@app.get("/api/calls/{call_id}/audio")
async def get_call_audio_url(call_id: str):
    print(f"Placeholder: /api/calls/{call_id}/audio hit")
    # This logic would use minio_client to generate a URL
    return {"url": "http://mock.url/audio.wav"}


@app.post("/api/chat/{call_id}")
async def chat_with_call(call_id: str, request: ChatRequest):
    print("Placeholder: /api/chat/{call_id} hit")
    return {"response": f"Mock AI response for call {call_id}"}
