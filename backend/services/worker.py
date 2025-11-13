# backend/services/worker.py
import logging
from config.logging_config import setup_logging
from config import db_config
from utils import redis_queue
from . import transcriber, analyzer


def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Worker started. Waiting for jobs...")
    while True:
        job = redis_queue.get_job_from_queue()
        # ... (job validation)
        call_id = job["call_id"]
        logger.info(f"\n--- PROCESSING JOB for call_id: {call_id} ---")

        try:
            # Set initial processing status
            db_config.update_call_status(call_id, "PROCESSING")

            call_doc = db_config.get_call_by_id(call_id)
            minio_path = call_doc.get("minio_path")

            # === Transcription Step ===
            db_config.update_call_status(call_id, "TRANSCRIBING")
            transcript = transcriber.transcribe_audio(minio_path)

            # === Analysis Step ===
            db_config.update_call_status(call_id, "ANALYZING")
            analysis_results = analyzer.analyze_transcript(transcript)

            # === Final Step ===
            db_config.save_analysis_results(
                call_id, analysis_results
            )  # This sets status to COMPLETED
            logger.info(f"--- SUCCESS: Job for {call_id} completed. ---")

        except Exception as e:
            logger.info(f"--- FAILED: Error processing job for {call_id}: {e} ---")
            db_config.update_call_status(call_id, "FAILED", error_message=str(e))


if __name__ == "__main__":
    main()
