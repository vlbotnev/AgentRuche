# backend/app.py
from fastapi import FastAPI, UploadFile, File
from contextlib import asynccontextmanager
from typing import List
from pydantic import BaseModel

# from config import settings, db
from utils import minio_client  # , redis_queue
# from tools import database_tools


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup...")
    minio_client.initialize_minio_bucket()
    yield
    print("Application shutdown...")


app = FastAPI(title="AgentRouche API", lifespan=lifespan)


# --- Placeholder Routers (can be split into files later) ---
class ChatRequest(BaseModel):
    query: str


@app.post("/api/calls/upload")
async def upload_calls(files: List[UploadFile] = File(...)):
    print("Placeholder: /api/calls/upload hit")
    return {"message": "Files uploaded successfully", "call_ids": ["mock_id_1"]}


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
