import os
import time
import threading
from pathlib import Path
from pyngrok import ngrok
from google.cloud import aiplatform
import google.auth
from langchain.llms import VertexAI

# Load Google Cloud credentials
creds, _ = google.auth.load_credentials_from_file("campusroute-key.json")
aiplatform.init(project="smartcampus-route", location="us-central1", credentials=creds)

# Initialize Vertex AI LLM
llm = VertexAI(
    model_name="gemini-1.5-pro",
    project="smartcampus-route",
    location="us-central1"
)

# Save Google API key into .env
GOOGLE_KEY = "YOUR_GOOGLE_KEY"
NGROK_KEY = "YOUR_NGROK_KEY"
Path(".env").write_text(f"GOOGLE_API_KEY={GOOGLE_KEY}\n")
os.system(f"ngrok config add-authtoken {NGROK_KEY}")

# Function to run Streamlit app
def run_streamlit():
    os.system("streamlit run app.py --server.address 0.0.0.0 --server.port 8501")

# Start Streamlit in background thread
threading.Thread(target=run_streamlit).start()
time.sleep(5)  # wait for server boot

# Open ngrok tunnel
public_url = ngrok.connect(8501)
print("🚀 CampusRoute App live at:", public_url)
