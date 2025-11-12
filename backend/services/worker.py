# backend/services/worker.py
import time


# This is your background worker that processes calls from the Redis queue.
def main():
    print("Worker started...")
    while True:
        time.sleep(5)
        print("Worker checking for jobs...")


if __name__ == "__main__":
    main()
