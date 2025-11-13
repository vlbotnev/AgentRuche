# backend/services/transcriber.py
import time


def transcribe_audio(minio_path: str) -> str:
    """Simulates transcribing an audio file."""
    print(f"STEP 1: Transcribing '{minio_path}'...")
    time.sleep(10)  # Simulate long-running transcription task
    transcript = f"This is a placeholder transcript for the file '{minio_path}'. The client mentioned the price was too high but agreed to a follow-up call next Tuesday."
    print("   -> Transcription complete.")
    return transcript
