import re
import spacy
from typing import List, Dict, Tuple
import pickle
from pathlib import Path
import os  # Import os to handle potential path issues

# Assuming mask_pii and predict_category are defined in models.py
try:
    from models import mask_pii, predict_category, Pipeline  # Import Pipeline if needed for type hinting
except ImportError:
    print("ERROR in utils.py: Could not import functions/classes from models.py")
    # Define dummy functions if import fails, so the rest of the file can load
    def mask_pii(text, nlp_model): return "Masking failed", []
    def predict_category(text, pipeline): return "Classification failed"
    Pipeline = object  # Dummy class

# --- Model Loading ---
MODEL_DIR = Path("saved_models")
MODEL_PATH = MODEL_DIR / "email_classifier_pipeline.pkl"
NLP_MODEL = None
MODEL_PIPELINE = None

def load_spacy_model():
    """Loads the spaCy model."""
    global NLP_MODEL
    if NLP_MODEL is None:
        try:
            NLP_MODEL = spacy.load("en_core_web_sm")
            print("spaCy model 'en_core_web_sm' loaded successfully.")
        except OSError:
            print("Error loading spaCy model 'en_core_web_sm'. Make sure it's downloaded.")
            # Attempt to download if not found (might fail in restricted envs)
            try:
                print("Attempting to download spaCy model...")
                spacy.cli.download("en_core_web_sm")
                NLP_MODEL = spacy.load("en_core_web_sm")
                print("spaCy model 'en_core_web_sm' downloaded and loaded successfully.")
            except Exception as download_e:
                print(f"Failed to download or load spaCy model: {download_e}")
                NLP_MODEL = None  # Ensure it remains None if loading fails
    return NLP_MODEL

def load_model_pipeline() -> Pipeline | None:
    """Loads the classification pipeline from the .pkl file."""
    global MODEL_PIPELINE
    if MODEL_PIPELINE is None:
        if not MODEL_PATH.exists():
            print(f"Model pipeline not found at {MODEL_PATH}. Please train and save the model pipeline first.")
            return None
        try:
            with open(MODEL_PATH, "rb") as f:
                MODEL_PIPELINE = pickle.load(f)
            print("Model pipeline loaded successfully.")
        except Exception as e:
            print(f"Error loading model pipeline from {MODEL_PATH}: {e}")
            MODEL_PIPELINE = None  # Ensure it remains None if loading fails
    return MODEL_PIPELINE

# --- PII Detection Regex Patterns ---
# Define regex patterns for PII entities not easily caught by NER
# (Refine these patterns carefully for accuracy)
REGEX_PATTERNS = {
    "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    "phone_number": r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',
    "credit_debit_no": r'\b(?:\d[ -]*?){13,16}\b',  # Basic pattern, needs refinement
    "cvv_no": r'\b\d{3,4}\b',  # Often needs context to differentiate
    "expiry_no": r'\b(0[1-9]|1[0-2])\/?([0-9]{4}|[0-9]{2})\b',  # MM/YY or MM/YYYY
    "aadhar_num": r'\b\d{4}[ -]?\d{4}[ -]?\d{4}\b',
    # DOB might be harder with regex alone, consider context or NER patterns
    "dob": r'\b(\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{4}[-/]\d{1,2}[-/]\d{1,2})\b'  # Basic DOB patterns
}

# --- PII Masking Function ---

def mask_pii(text: str) -> Tuple[str, List[Dict]]:
    """
    Detects and masks PII in the input text using spaCy NER and Regex.

    Args:
        text: The input email body string.

    Returns:
        A tuple containing:
        - masked_email (str): The email body with PII replaced by placeholders.
        - list_of_masked_entities (List[Dict]): A list of dictionaries,
          each detailing a masked entity (position, classification, original value).
    """
    masked_text = text
    list_of_masked_entities = []
    found_spans = []  # To store (start, end, entity_type, original_value)

    # 1. Use spaCy for Named Entity Recognition (PERSON for full_name)
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            # Simple PERSON check, might need refinement (e.g., filter short names)
            if len(ent.text.split()) > 1:  # Basic check for multi-word names
                found_spans.append((ent.start_char, ent.end_char, "full_name", ent.text))

    # 2. Use Regex for other PII types
    for entity_type, pattern in REGEX_PATTERNS.items():
        for match in re.finditer(pattern, text):
            # Basic check for overlap with already found spans (can be improved)
            is_overlapping = any(
                max(found[0], match.start()) < min(found[1], match.end())
                for found in found_spans
            )
            if not is_overlapping:
                # Add basic context checks if needed (e.g., for CVV)
                # if entity_type == "cvv_no" and not is_likely_cvv(text, match): continue
                found_spans.append((match.start(), match.end(), entity_type, match.group(0)))

    # 3. Sort spans by start position to handle masking correctly
    found_spans.sort(key=lambda x: x[0])

    # 4. Perform masking and create the entity list
    offset = 0  # Keep track of index changes due to replacements
    for start, end, entity_type, original_value in found_spans:
        adjusted_start = start + offset
        adjusted_end = end + offset
        placeholder = f"[{entity_type}]"

        # Replace the PII with the placeholder in the masked_text
        masked_text = masked_text[:adjusted_start] + placeholder + masked_text[adjusted_end:]

        # Update the offset for subsequent replacements
        offset += len(placeholder) - (end - start)

        # Add details to the list_of_masked_entities
        list_of_masked_entities.append({
            "position": [start, end],  # Use ORIGINAL indices
            "classification": entity_type,
            "entity": original_value
        })

    # Sort the final list by original start position for consistency
    list_of_masked_entities.sort(key=lambda x: x["position"][0])

    return masked_text, list_of_masked_entities

# --- Main Processing Function for Gradio ---

def process_email_request(email_body: str) -> dict:
    """
    Processes the input email body for PII masking and classification.
    Loads models on first call if not already loaded.
    """
    print("Processing email request...")  # Add log
    nlp = load_spacy_model()
    pipeline = load_model_pipeline()

    if nlp is None:
        return {"error": "spaCy model not loaded.", "input_email_body": email_body}
    if pipeline is None:
        return {"error": "Classification pipeline not loaded.", "input_email_body": email_body}

    try:
        # 1. Mask PII using the loaded spaCy model
        # Ensure mask_pii expects the nlp model as an argument if needed
        masked_email_body, entities = mask_pii(email_body, nlp)  # Pass nlp model
        print(f"PII Masking complete. Found {len(entities)} entities.")  # Add log

        # Convert entities to the required dict format if necessary
        # Assuming mask_pii already returns entities as list of dicts
        # with 'position', 'classification', 'entity' keys.

        # 2. Classify the masked email using the loaded pipeline
        predicted_class = predict_category(masked_email_body, pipeline)
        print(f"Classification complete. Predicted class: {predicted_class}")  # Add log

        # 3. Construct the response dictionary
        response = {
            "input_email_body": email_body,
            "list_of_masked_entities": entities,  # Ensure this matches expected format
            "masked_email": masked_email_body,
            "category_of_the_email": predicted_class
        }
        print("Response constructed successfully.")  # Add log
        return response

    except Exception as e:
        print(f"Error during email processing: {e}")  # Log the specific error
        # Consider logging the full traceback for debugging
        # import traceback
        # print(traceback.format_exc())
        return {
            "error": f"An error occurred during processing: {str(e)}",
            "input_email_body": email_body
        }

# --- Other Utility Functions (Add as needed) ---
# E.g., text cleaning for classification model input
def clean_text_for_classification(text: str) -> str:
    """Basic text cleaning."""
    text = text.lower()
    text = re.sub(r'<.*?>', '', text)  # Remove HTML tags
    text = re.sub(r'[^a-z\s]', '', text)  # Remove punctuation/numbers (adjust if needed)
    text = re.sub(r'\s+', ' ', text).strip()  # Normalize whitespace
    # Add stopword removal if necessary (import nltk stopwords)
    return text
