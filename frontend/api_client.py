import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Read backend URL strictly from environment variable as required by specifications
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def check_backend_health() -> bool:
    """Verifies that the FastAPI backend service is reachable."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=3)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def query_rag_assistant(question: str) -> dict:
    """Sends user question to the backend and returns the grounded answer with citations."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/query",
            json={"question": question},
            timeout=120
        )
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 422:
            return {"error": "Invalid question input. Please enter a valid non-empty query."}
        else:
            return {"error": f"Backend returned error code: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to connect to the backend server: {str(e)}"}