# filepath: /workspaces/internship1/app.py
import uvicorn
import os

# Import the FastAPI app instance from api.py
# Ensure the FastAPI instance in api.py is named 'app'
try:
    from api import app
except ImportError:
    print("Error: Could not import 'app' from api.py.")
    print("Make sure api.py exists and contains a FastAPI instance named 'app'.")
    app = None
except Exception as e:
    print(f"An unexpected error occurred during import: {e}")
    app = None


if __name__ == "__main__":
    if app:
        # Get port from environment variable PORT, default to 8000
        # Hugging Face Spaces and other platforms often set the PORT variable
        port = int(os.environ.get("PORT", 8000))
        # Use host="0.0.0.0" to make it accessible externally (in Codespaces/Docker/HF)
        print(f"Starting Uvicorn server on host 0.0.0.0, port {port}")
        uvicorn.run(app, host="0.0.0.0", port=port)
    else:
        print("Could not start server because the FastAPI app instance was not loaded.")