import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from typing import Tuple, Any, Optional, List, Dict
from pathlib import Path
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils import clean_text_for_classification
import spacy
import pickle

# --- Constants ---
MODEL_DIR = Path("saved_models")
MODEL_PATH = MODEL_DIR / "email_classifier_pipeline.pkl"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# --- FastAPI App ---
app = FastAPI()

# --- Pydantic Models for Request/Response ---
class EmailInput(BaseModel):
    email_body: str

class MaskedEntity(BaseModel):
    position: List[int]
    classification: str
    entity: str

class ClassificationOutput(BaseModel):
    input_email_body: str
    list_of_masked_entities: List[MaskedEntity]
    masked_email: str
    category_of_the_email: str

# --- Load Model at Startup ---
# Load the model pipeline once when the application starts
model_pipeline: Optional[Pipeline] = None

# --- Model Loading ---
def load_model_pipeline() -> Optional[Pipeline]:
    """Loads the trained model pipeline."""
    model_pipeline = None
    if MODEL_PATH.exists():
        try:
            model_pipeline = joblib.load(MODEL_PATH)
            print(f"Model pipeline loaded successfully from {MODEL_PATH}")
        except Exception as e:
            print(f"Error loading model pipeline from {MODEL_PATH}: {e}")
    else:
        print(f"Model pipeline not found at {MODEL_PATH}.")
        print("Please train and save the model pipeline first.")
    return model_pipeline

# --- Mask PII Function ---
def mask_pii(text: str, nlp_model: spacy.language.Language) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Finds and masks PII entities in text using the provided spaCy model.

    Args:
        text: The input email body.
        nlp_model: The loaded spaCy language model.

    Returns:
        A tuple containing:
            - The email body with PII entities replaced by placeholders (e.g., "[full_name]").
            - A list of dictionaries, where each dictionary describes a masked entity
              (e.g., {"position": [start, end], "classification": "entity_type", "entity": "original_text"}).
    """
    print(f"Executing mask_pii for text: '{text[:50]}...'") # Add log
    masked_text = text
    entities = []
    doc = nlp_model(text)
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "EMAIL"]:
            entity_info = {
                "position": [ent.start_char, ent.end_char],
                "classification": ent.label_.lower(),
                "entity": ent.text
            }
            entities.append(entity_info)
            masked_text = masked_text.replace(ent.text, f"[{ent.label_.lower()}]")
    print(f"mask_pii result - entities: {entities}") # Add log
    return masked_text, entities

# --- Prediction Function ---
def predict_category(text: str, pipeline: Pipeline) -> str:
    """
    Predicts the category of the text using the loaded classification pipeline.

    Args:
        text: The input text (potentially masked).
        pipeline: The loaded scikit-learn compatible pipeline object.

    Returns:
        The predicted category name as a string.
    """
    print(f"Executing predict_category for text: '{text[:50]}...'") # Add log
    try:
        prediction = pipeline.predict([text])
        category = str(prediction[0]) if prediction else "Prediction failed"
    except Exception as e:
        print(f"Error during prediction: {e}")
        category = "Prediction Error"
    print(f"predict_category result: {category}") # Add log
    return category

# --- Training Function ---
def train_model(data_path: Path, model_save_path: Path):
    """Loads data, trains the model pipeline, and saves it."""

    if not data_path.exists():
        print(f"Error: Dataset not found at {data_path}")
        print("Please make sure the CSV file is uploaded to your Codespace.")
        return

    print(f"Loading dataset from {data_path}...")
    try:
        df = pd.read_csv(data_path)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return

    # --- Data Validation ---
    email_body_column = 'body'       # Column name for email text in your CSV
    category_column = 'category'     # Column name for the category label in your CSV

    if email_body_column not in df.columns:
        print(f"Error: Email body column '{email_body_column}' not found in the dataset.")
        print(f"Available columns: {df.columns.tolist()}")
        return
    if category_column not in df.columns:
        print(f"Error: Category column '{category_column}' not found in the dataset.")
        print(f"Available columns: {df.columns.tolist()}")
        return

    # Handle potential missing values
    df.dropna(subset=[email_body_column, category_column], inplace=True)
    if df.empty:
        print("Error: No valid data remaining after handling missing values.")
        return

    print("Applying text cleaning...")
    # Ensure the cleaning function exists and works
    try:
        df['cleaned_text'] = df[email_body_column].astype(str).apply(clean_text_for_classification)
    except Exception as e:
        print(f"Error during text cleaning: {e}")
        return

    print("Splitting data...")
    X = df['cleaned_text']
    y = df[category_column]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y # Use stratify for balanced splits
    )

    # --- Model Pipeline ---
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english', max_df=0.95, min_df=2)),
        ('clf', MultinomialNB()) # Using Naive Bayes as a starting point
    ])

    print("Training model...")
    try:
        pipeline.fit(X_train, y_train)
        print("Training complete.")
    except Exception as e:
        print(f"Error during model training: {e}")
        return

    # --- Evaluation ---
    try:
        accuracy = pipeline.score(X_test, y_test)
        print(f"Model Accuracy on Test Set: {accuracy:.4f}")
    except Exception as e:
        print(f"Error during model evaluation: {e}")


    # --- Save Model ---
    print(f"Saving model pipeline to {model_save_path}...")
    model_save_path.parent.mkdir(parents=True, exist_ok=True) # Ensure directory exists
    try:
        joblib.dump(pipeline, model_save_path)
        print("Model pipeline saved successfully.")
    except Exception as e:
        print(f"Error saving model pipeline: {e}")

# --- API Endpoints ---
@app.get("/")
def read_root():
    return {"message": "Email Classification API is running. Use the /classify/ endpoint."}

@app.post("/classify/", response_model=ClassificationOutput)
async def classify_email(email_input: EmailInput):
    if model_pipeline is None:
        raise HTTPException(status_code=503, detail="Model not loaded. API is not ready.")

    input_email = email_input.email_body

    # 1. Mask PII
    masked_text, masked_entities_list = mask_pii(input_email)

    # Convert masked_entities_list to list of MaskedEntity objects if needed
    # (Depends on how mask_pii returns it, ensure structure matches Pydantic model)
    formatted_entities = [MaskedEntity(**entity) for entity in masked_entities_list]

    # 2. Predict Category using the masked text
    predicted_category = predict_category(masked_text, model_pipeline)

    # 3. Construct and return the response
    response = ClassificationOutput(
        input_email_body=input_email,
        list_of_masked_entities=formatted_entities,
        masked_email=masked_text,
        category_of_the_email=predicted_category
    )
    return response

# Example Usage (if you run this file directly for testing/training)
if __name__ == "__main__":
    print("Running models.py directly...")
    dummy_emails = [
        "Subject: Billing Issue My account [full_name] was charged twice for order [order_id]. Please refund.",
        "Subject: Help needed Cannot login. My email is [email]. Reset password link broken.",
        "Subject: Account Management Request to close my account [account_num]. User [full_name]."
        ]
    dummy_labels = ["Billing Issues", "Technical Support", "Account Management"]

    print("Attempting to load model and predict...")
    model_pipeline = load_model_pipeline()
    if model_pipeline:
        test_email = "my login is not working help required email [email]"
        category = predict_category(test_email, model_pipeline)
        print(f"Test Email: '{test_email}'")
        print(f"Predicted Category: {category}")
    else:
        print("Cannot perform prediction as model pipeline failed to load.")
#hi i am siddharth
#hi i am siddharth