# Use this file to better understand the capstone workflow

## 1. Project Overview

Our goal is to build a full-stack AI application that can ingest audio recordings of phone calls, transcribe them, and provide deep analytics to help a business (like a call center) improve its operations.

### Key Components

* **Frontend (`/frontend`):** A Streamlit dashboard for users to upload files and view analytics.
* **Backend (`/backend`):** A FastAPI server that provides a REST API for all operations (uploading, fetching data, chatting).
* **Worker (`/backend/services/worker.py`):** A background process that does the heavy lifting: transcribing audio and running AI analysis using LangChain.
* **Databases & Services (Managed by Docker):**
  * **MongoDB:** Stores all metadata about calls (transcripts, analytics, status).
  * **Minio:** Stores the raw audio files.
  * **Redis:** A message queue that assigns processing jobs to the worker.

## 2. Getting Started: Running the Project Locally

Follow these steps to get the entire application running on your machine.

### Prerequisites

* **Docker Desktop:** Make sure it's installed and running.
* **uv:** Our Python package manager. [Installation Guide](https://github.com/astral-sh/uv)

#### Step-by-Step Guide

1. **Clone the Repository:**

    ```bash
    git clone git@github.com:vlbotnev/AgentRuche.git
    cd AgentRuche
    ```

2. **Create Your Environment File:**
    This is the most important step. Copy the example file and fill in your unique API key.

    ```bash
    cp .env.example .env
    ```

    Or copy using more convinient for you way

    Now, open the `.env` file and paste our `GOOGLE_API_KEY` from whatsapp message I've sent.

3. **Launch Everything with Docker Compose:**
    This single command will build the containers for the frontend and backend, and pull the images for our databases.

    ```bash
    docker-compose up --build -d
    ```

    The `-d` runs it in detached mode (in the background). To see logs, run `docker-compose logs -f backend` or `docker-compose logs -f frontend`.

4. **Verify Services are Running:**
    * **Frontend App:** Open [http://localhost:8505](http://localhost:8505)
    * **Backend API Docs:** Open [http://localhost:8002/docs](http://localhost:8002/docs)
    * **Minio File Storage:** Open [http://localhost:9006](http://localhost:9006)
    * **MongoDB & Redis** are running but don't have a web UI. See the next section for how to connect.

## 3. Connecting to Our Services (The User-Friendly Way)

To see what's happening inside our databases, you'll need a GUI client for each. This is the easiest way to inspect data.

* **Minio (For Audio Files)**
    1. **How to Connect:** Just open **[http://localhost:9006](http://localhost:9006)** in your browser.
    2. **Credentials:** Use the `MINIO_USER` and `MINIO_PASS` from your `.env` file.
    3. **What you'll see:** You can browse "buckets" (folders). Our app will automatically create the `recordings` bucket, and you'll see all uploaded audio files there.

* **MongoDB (For Call Data & Analytics)**
    1. **Recommended Tool:** Download and install [MongoDB Compass](https://www.mongodb.com/products/compass).
    2. **How to Connect:**
        * Open Compass and click "New Connection".
        * Paste this connection string: `mongodb://admin:password@localhost:27021/` (Use the credentials from your `.env` file).
    3. **What you'll see:** You will find our `call_analyzer` database and inside it, a `calls` collection. Each document in this collection represents a single phone call with its transcript and all the AI analytics we've extracted.

* **Redis (For the Job Queue)**
    > You won't probably need to use Redis in your work so don't bother installing it
    1. **Recommended Tool:** Download and install [RedisInsight](https://redis.com/redis-enterprise/redis-insight/).
    2. **How to Connect:**
        * Open RedisInsight and click "Add Redis Database".
        * Choose "Add Database Manually".
        * **Host:** `localhost`
        * **Port:** `6399`
    3. **What you'll see:** You can browse the keys. When you upload a file, you'll briefly see a job appear in a list named `call_processing_queue`. This is how the backend tells the worker what to do.

## 4. Managing Dependencies with `uv`

Our project is split into two sub-projects (`backend` and `frontend`), each with its own dependencies.

* **To Add a New Package (e.g., to the backend):**

    ```bash
    cd backend
    uv add <package-name>
    ```

    Same for frontend

    This will automatically update your `pyproject.toml`.

* **To Install All Packages After a `git pull`:**
    If a teammate added a new package, you just need to sync.

    ```bash
    cd backend
    uv sync
    ```

    Same for frontend

## 5. Backend Development Workflow

This is how you add new features to the project.

### A. How to Add a New API Endpoint

Let's say we want an endpoint to get all calls for a specific operator. Using frontend
> Note: This is for frontend if you want to add same function calling option, go to section D

1. **Open `backend/app.py`**.
2. Add a new function using the FastAPI decorator. The function should call our database logic.

    ```python
    # backend/app.py
    from config.db_config import calls_collection

    # ... other endpoints ...

    @app.get("/api/calls/operator/{operator_name}")
    async def get_calls_by_operator(operator_name: str):
        """
        Finds all calls associated with a specific operator.
        """
        # We will use our database instance to find the data
        calls = calls_collection.find({"operator_name": operator_name})
        
        # Convert MongoDB cursor to a list of dicts
        # Note: You'll need a helper function to handle ObjectId you can use mongo_list_to_dict_list from backend/utils/mongo_helpers.py to do this
        return list(calls)
    ```

3. **Test it!** After Docker rebuilds, go to the API docs at [http://localhost:8002/docs](http://localhost:8002/docs), find your new endpoint, and try it out.

### B. How to Work with the Database (CRUD)

All database logic uses the `calls_collection` instance we import from `backend/config/db_config.py`.

```python
# Import it in any file you need it
from config.db_config import calls_collection
from bson.objectid import ObjectId # Important for finding by ID

# --- CREATE ---
def create_new_call(filename, operator):
    new_call = {"filename": filename, "operator_name": operator, "status": "PENDING"}
    result = calls_collection.insert_one(new_call)
    return str(result.inserted_id)

# --- READ ---
def find_call_by_id(call_id: str):
    # Convert string ID to MongoDB's ObjectId
    return calls_collection.find_one({"_id": ObjectId(call_id)})

# --- UPDATE ---
def update_call_status(call_id: str, new_status: str):
    calls_collection.update_one(
        {"_id": ObjectId(call_id)},
        {"$set": {"status": new_status}}
    )

# --- DELETE ---
def delete_call(call_id: str):
    calls_collection.delete_one({"_id": ObjectId(call_id)})

```

### C. How to Add a New LLM Analytic (for the Call Processor)

This logic runs in the background worker. The main file to edit is `backend/services/analyzer.py`.

Let's add "Sentiment Analysis".

1. **Create the AI Logic:** In `backend/services/analyzer.py`, create a new function that takes the transcript and returns the sentiment. We'll imagine the LangChain code.

    ```python
    # backend/services/analyzer.py

    # You would import your LLM and prompt templates here
    # from langchain_google_genai import ChatGoogleGenerativeAI
    # llm = ChatGoogleGenerativeAI(model="gemini-pro")

    def extract_sentiment(transcript: str) -> str:
        """Uses an LLM to determine if the call sentiment was POSITIVE, NEGATIVE, or NEUTRAL."""
        print("Extracting sentiment...")
        # Imagine a LangChain prompt and chain that returns one of the three options
        # result = llm.invoke("Analyze this transcript... and return only POSITIVE, NEGATIVE, or NEUTRAL: " + transcript)
        # return result.content
        return "POSITIVE" # Placeholder
    
    # ... other analysis functions ...
    ```

2. **Integrate it into the Main Analyzer:** Call your new function from the main `analyze_transcript` function and add its result to the dictionary.

    ```python
    # backend/services/analyzer.py

    def analyze_transcript(transcript: str) -> dict:
        """Runs the full analysis pipeline on a transcript."""
        # ... existing analysis for entities, summary etc. ...
        
        # Call your new function
        sentiment = extract_sentiment(transcript)

        # Return the combined results
        return {
            "full_transcript": transcript,
            # ... other results ...
            "sentiment": sentiment # <-- Add the new data point
        }
    ```

3. **That's it!** The worker (`services/worker.py`) calls `analyze_transcript`, and the result is automatically saved to MongoDB with the new `sentiment` field.

### D. How to Add a New Chat Capability (Function Calling Tool)

This allows our chat AI to get information from our database. The main file to edit is `backend/tools/database_tools.py`.

Let's add the tool for the endpoint we created earlier: "Find calls by operator".

1. **Define the Tool:** A tool is just a Python function with a very clear docstring. The LLM reads the docstring to understand what the tool does.

    ```python
    # backend/tools/database_tools.py
    from config.db_config import calls_collection

    def get_calls_by_operator_name(operator_name: str) -> list[dict]:
        """
        Searches the database and returns a list of all calls made by a specific operator. 
        Use this to answer questions like 'How many calls did John make?' or 'Show me Jane's calls'.
        """
        print(f"TOOL EXECUTED: Searching for calls by {operator_name}")
        
        # Use our database logic
        calls = calls_collection.find({"operator_name": operator_name})
        
        # You'll need a helper to convert MongoDB docs to JSON-serializable dicts
        return list(calls) 
    ```

2. **Register the Tool with the Agent:** In the file where the LangChain chat agent is defined (e.g., in a future `services/chat_service.py`), you would import and add this tool to the agent's list of available tools.

    ```python
    # This is conceptual code for a future chat service file
    from langchain.agents import AgentExecutor, create_react_agent
    from tools.database_tools import get_calls_by_operator_name

    # The agent will have a list of tools it can use
    tools = [
        get_calls_by_operator_name,
        # ... other tools ...
    ]

    # ... agent creation logic ...
    ```

Now, when a user asks the chat, "Show me all of John Smith's calls," the agent will see your new tool, understand that it can answer the question, and execute it.
