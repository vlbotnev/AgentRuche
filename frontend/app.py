# frontend/app.py
import streamlit as st
import os
import requests

# Load backend URL from environment variables for flexibility
BACKEND_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")

st.title("Call Analyzer Dashboard")

st.header("Upload Audio Files")
uploaded_files = st.file_uploader("Choose WAV or MP3 files", accept_multiple_files=True)

if uploaded_files:
    if st.button("Upload and Process"):
        with st.spinner("Uploading files..."):
            # The 'files' parameter for requests needs a list of tuples
            files_to_upload = [
                ("files", (file.name, file.getvalue(), file.type))
                for file in uploaded_files
            ]
            try:
                response = requests.post(
                    f"{BACKEND_URL}/api/calls/upload", files=files_to_upload
                )
                if response.status_code == 200:
                    st.success("Files uploaded successfully!")
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except requests.exceptions.ConnectionError as e:
                st.error(
                    f"Connection Error: Could not connect to the backend at {BACKEND_URL}. Is it running?"
                )


st.header("Processed Calls")
# In a real app, you would fetch this data from the backend /api/calls endpoint
st.table(
    {
        "Filename": ["call_1.wav", "call_2.wav"],
        "Status": ["Completed", "Processing..."],
        "Operator": ["John Doe", "Jane Smith"],
    }
)
