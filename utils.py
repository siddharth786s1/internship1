import re
import spacy
from typing import List, Dict, Tuple

# Load the spaCy model once when the module is loaded
# Using disable=['parser', 'lemmatizer'] can speed it up if you only need NER
try:
    nlp = spacy.load("en_core_web_sm", disable=['parser', 'lemmatizer'])
    print("spaCy model 'en_core_web_sm' loaded successfully.")
except OSError:
    print("Downloading 'en_core_web_sm' model...")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm", disable=['parser', 'lemmatizer'])
    print("spaCy model 'en_core_web_sm' loaded successfully after download.")


# --- PII Detection Regex Patterns ---
# Define regex patterns for PII entities not easily caught by NER
# (Refine these patterns carefully for accuracy)
REGEX_PATTERNS = {
    "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    "phone_number": r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',
    "credit_debit_no": r'\b(?:\d[ -]*?){13,16}\b', # Basic pattern, needs refinement
    "cvv_no": r'\b\d{3,4}\b', # Often needs context to differentiate
    "expiry_no": r'\b(0[1-9]|1[0-2])\/?([0-9]{4}|[0-9]{2})\b', # MM/YY or MM/YYYY
    "aadhar_num": r'\b\d{4}[ -]?\d{4}[ -]?\d{4}\b',
    # DOB might be harder with regex alone, consider context or NER patterns
    "dob": r'\b(\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{4}[-/]\d{1,2}[-/]\d{1,2})\b' # Basic DOB patterns
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
    found_spans = [] # To store (start, end, entity_type, original_value)

    # 1. Use spaCy for Named Entity Recognition (PERSON for full_name)
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            # Simple PERSON check, might need refinement (e.g., filter short names)
            if len(ent.text.split()) > 1: # Basic check for multi-word names
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
    offset = 0 # Keep track of index changes due to replacements
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
            "position": [start, end], # Use ORIGINAL indices
            "classification": entity_type,
            "entity": original_value
        })

    # Sort the final list by original start position for consistency
    list_of_masked_entities.sort(key=lambda x: x["position"][0])

    return masked_text, list_of_masked_entities

# --- Other Utility Functions (Add as needed) ---
# E.g., text cleaning for classification model input
def clean_text_for_classification(text: str) -> str:
    """Basic text cleaning."""
    text = text.lower()
    text = re.sub(r'<.*?>', '', text) # Remove HTML tags
    text = re.sub(r'[^a-z\s]', '', text) # Remove punctuation/numbers (adjust if needed)
    text = re.sub(r'\s+', ' ', text).strip() # Normalize whitespace
    # Add stopword removal if necessary (import nltk stopwords)
    return text
