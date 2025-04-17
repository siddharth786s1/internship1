from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Tuple, Any, Optional
import os  # To potentially load environment variables if needed

# Make sure these imports work and don't cause errors themselves
try:
    from utils import mask_pii
    from models import load_model_pipeline, predict_category, Pipeline  # Ensure Pipeline is imported if type hint used
except ImportError as e:
    print(f"Error importing from utils or models in api.py: {e}")
    # Optionally raise the error to make it obvious during startup
    # raise e
except Exception as e:
    print(f"Unexpected error during imports in api.py: {e}")
    # raise e

# --- FastAPI App ---
# >>>>> THIS LINE IS CRUCIAL <<<<<
app = FastAPI()
# >>>>> MUST BE NAMED 'app' <<<<<

# --- Pydantic Models ---
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

# --- Load Model at Startup ---
# Ensure load_model_pipeline() exists and works
model_pipeline: Optional[Pipeline] = load_model_pipeline()

# --- API Endpoints ---
@app.get("/")
async def read_root():
    return {"message": "Email Classification API is running. Use the /classify/ endpoint."}

@app.post("/classify/", response_model=ClassificationOutput)
async def classify_email(email_input: EmailInput):
    """
    Accepts an email body, masks PII, classifies the email,
    and returns the results in the specified JSON format.
    """
    if not model_pipeline:
        raise HTTPException(status_code=503, detail="Model pipeline not available. Please train/load it first.")

    input_email = email_input.email_body

    try:
        # 1. Mask PII
        masked_email_body, entities = mask_pii(input_email)

        # Ensure entities match the Pydantic model format
        validated_entities = [MaskedEntity(**entity) for entity in entities]

        # 2. Classify the masked email
        predicted_class = predict_category(masked_email_body, model_pipeline)

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
