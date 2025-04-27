# filepath: /workspaces/internship1/app.py
import uvicorn
import os
import gradio as gr

import json

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

# Assumption: 'process_email_request' is the function that takes email text
# and returns the dictionary with keys like 'input_email_body', 'list_of_masked_entities', etc.
# Adjust the import based on where this function is defined (e.g., utils.py, api.py)
try:
    from utils import process_email_request # MAKE SURE THIS IMPORT IS CORRECT
    print("Successfully imported process_email_request from utils.")
except ImportError:
    print("Could not import process_email_request from utils. Trying from api...")
    try:
        # If the logic is maybe within api.py but callable
        from api import process_email_request # MAKE SURE THIS IMPORT IS CORRECT
        print("Successfully imported process_email_request from api.")
    except ImportError:
        print("ERROR: Could not find the core processing function 'process_email_request'.")
        print("Please ensure it's defined and importable from utils.py or api.py")
        # Define a dummy function so Gradio doesn't crash immediately
        def process_email_request(email_body):
            return {"error": "Processing function not found.", "input_email_body": email_body}

# Define the Gradio interface
iface = gr.Interface(
    fn=process_email_request,
    inputs=gr.Textbox(lines=15, label="Input Email Body", placeholder="Paste email content here..."),
    outputs=gr.JSON(label="Processing Results"),
    title="Email Classification and PII Masking API",
    description="Enter the body of an email below. The API will process it to mask PII entities (like names, emails) and classify the email's category. The results will be shown in JSON format.",
    flagging_mode="never" # Changed from allow_flagging
)

# Launch the interface
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
    iface.launch() # Share=False is default, suitable for HF Spaces