from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Tuple # Added Tuple
import os # To potentially load environment variables if needed

# Import functions from our modules
from utils import mask_pii
from models import load_model_and_vectorizer, predict_category

# --- API Initialization ---
app = FastAPI(
    title="Email Classification API",
    description="Classifies support emails and masks PII.",
    version="1.0.0"
)

# --- Data Models for Request and Response ---
class EmailInput(BaseModel):
    email_body: str = Field(..., example="Hello, my name is Jane Doe and my email is jane.doe@example.com. I have a billing question.")

class MaskedEntity(BaseModel):
    position: List[int] = Field(..., example=[18, 26])
    classification: str = Field(..., example="full_name")
    entity: str = Field(..., example="Jane Doe")

class ClassificationOutput(BaseModel):
    input_email_body: str
    list_of_masked_entities: List[MaskedEntity]
    masked_email: str
    category_of_the_email: str

# --- Load Models on Startup ---
# This ensures the model is loaded once when the API starts, not per request
model, vectorizer = load_model_and_vectorizer()

# --- API Endpoint ---
@app.post("/classify/", response_model=ClassificationOutput)
async def classify_email(email_input: EmailInput):
    """
    Accepts an email body, masks PII, classifies the email,
    and returns the results in the specified JSON format.
    """
    if not model or not vectorizer:
        raise HTTPException(status_code=503, detail="Model or Vectorizer not available. Please train/load them first.")

    input_email = email_input.email_body

    try:
        # 1. Mask PII
        masked_email_body, entities = mask_pii(input_email)

        # Ensure entities match the Pydantic model format
        validated_entities = [MaskedEntity(**entity) for entity in entities]

        # 2. Classify the masked email
        predicted_class = predict_category(masked_email_body, model, vectorizer)

        # 3. Construct the response
        response = ClassificationOutput(
            input_email_body=input_email,
            list_of_masked_entities=validated_entities,
            masked_email=masked_email_body,
            category_of_the_email=predicted_class
        )
        return response

    except Exception as e:
        # Log the exception for debugging
        print(f"Error processing request: {e}")
        # Optionally include more detail in the error response during development
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# --- Root Endpoint (Optional - for basic check) ---
@app.get("/")
async def root():
    return {"message": "Email Classification API is running. Use the /classify/ endpoint."}

# --- Running the API (for local development) ---
# You'll typically run this using uvicorn from the terminal:
# uvicorn api:app --reload
# The block below is useful if you want to run `python api.py` directly sometimes,
# but `uvicorn` command is standard for development.
if __name__ == "__main__":
    import uvicorn
    print("Starting Uvicorn server directly (for debugging)...")
    # Use host="0.0.0.0" to make it accessible within Codespace network
    uvicorn.run(app, host="0.0.0.0", port=8000)
