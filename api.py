print("Importing api.py...") # Add print statement

# --- Define/Import Pipeline Type FIRST ---
try:
    from sklearn.pipeline import Pipeline
    print("api.py: Imported Pipeline from sklearn.")
except ImportError:
    Pipeline = object  # type: ignore
    print("api.py: Defined fallback Pipeline type.")

# --- Other Imports ---
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Tuple, Any, Optional, Union
import sys
import os

# --- Import from utils (AFTER Pipeline is defined) ---
try:
    # utils.py should now import without circular dependency issues
    from utils import process_email_request, load_spacy_model, load_model_pipeline
    print("api.py: Successfully imported from utils.")
except ImportError as e:
    print(f"ERROR in api.py: Could not import from utils. Details: {e}")
    # Define dummy functions if import fails
    def process_email_request(email_body: str): 
        return {"error": f"Failed to import processing function: {e}"}
    def load_spacy_model(): 
        print("Dummy spacy loader called")
        return None
    def load_model_pipeline(): 
        print("Dummy pipeline loader called")
        return None

app = FastAPI(title="Email PII Classifier API", version="1.0.0")

class EmailInput(BaseModel):
    email_body: str = Field(..., example="Hello, my name is Jane Doe and my email is jane.doe@example.com. I have a billing question.")

class MaskedEntity(BaseModel):
    position: List[int] = Field(..., example=[18, 26])
    classification: str = Field(..., example="full_name")
    entity: str = Field(..., example="Jane Doe")

class EmailResponse(BaseModel):
    input_email_body: str
    list_of_masked_entities: List[MaskedEntity]
    masked_email: str
    category_of_the_email: str

# --- Load models on startup ---
@app.on_event("startup")
async def startup_event():
    print("FastAPI startup: Loading models...")
    load_spacy_model()       # Load spaCy model
    load_model_pipeline()    # Load classification pipeline
    print("FastAPI startup: Model loading complete.")

# --- API Endpoint ---
@app.post("/classify_email/", response_model=Union[EmailResponse, Dict[str, str]])  # Allow dict for error response
async def classify_email(email_input: EmailInput):
    """
    Receives email body, performs PII masking and classification.
    """
    try:
        print("Received request for /classify_email/")  # Log request
        result = process_email_request(email_input.email_body)

        if "error" in result:
            # Return a 500 error if processing failed internally
            raise HTTPException(status_code=500, detail=result["error"])

        # Validate response structure before returning (optional but good practice)
        # This assumes process_email_request returns the correct structure on success
        return EmailResponse(**result)

    except HTTPException as http_exc:
        # Re-raise HTTP exceptions (like the 500 error above)
        raise http_exc
    except Exception as e:
        print(f"Unexpected error in /classify_email endpoint: {e}")
        # import traceback # Uncomment for detailed debugging
        # print(traceback.format_exc()) # Uncomment for detailed debugging
        # Return a generic 500 error for other unexpected issues
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {str(e)}")

# --- Root Endpoint ---
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Email PII Classifier API. Use the /docs endpoint for details."}

print("api.py finished importing.") # Add print statement

# --- Optional: Add uvicorn runner for local testing ---
if __name__ == "__main__":
    import uvicorn
    print("Starting Uvicorn server directly (for debugging)...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
