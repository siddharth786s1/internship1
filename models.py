import joblib
from pathlib import Path
from typing import Any # For type hinting the model/vectorizer
from utils import clean_text_for_classification # Import cleaning function

# --- Configuration ---
MODEL_DIR = Path("saved_models")
MODEL_PATH = MODEL_DIR / "email_classifier.joblib"
VECTORIZER_PATH = MODEL_DIR / "tfidf_vectorizer.joblib"

# Ensure the model directory exists
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# --- Placeholder for Model Loading ---
# In a real scenario, you'd train and save these first.
# For now, we'll define functions to load them, assuming they exist.

def load_model_and_vectorizer() -> Tuple[Any, Any]:
    """Loads the saved classification model and vectorizer."""
    model = None
    vectorizer = None

    if MODEL_PATH.exists() and VECTORIZER_PATH.exists():
        try:
            model = joblib.load(MODEL_PATH)
            vectorizer = joblib.load(VECTORIZER_PATH)
            print("Model and vectorizer loaded successfully.")
        except Exception as e:
            print(f"Error loading model or vectorizer: {e}")
            # Handle error appropriately, maybe raise it or return None
    else:
        print(f"Model ({MODEL_PATH}) or Vectorizer ({VECTORIZER_PATH}) not found.")
        print("Please train and save the model and vectorizer first.")
        # In a real app, you might trigger training or raise an error
        # For this template, we'll proceed with None, API will handle it

    return model, vectorizer

# --- Prediction Function ---
def predict_category(text: str, model: Any, vectorizer: Any) -> str:
    """
    Predicts the email category using the loaded model and vectorizer.

    Args:
        text: The masked email text.
        model: The loaded classification model.
        vectorizer: The loaded text vectorizer.

    Returns:
        The predicted category name (str) or a default/error string.
    """
    if not model or not vectorizer:
        return "Error: Model or Vectorizer not loaded"

    try:
        # 1. Clean the masked text
        cleaned_text = clean_text_for_classification(text)

        # 2. Vectorize the cleaned text
        # Note: vectorizer.transform expects an iterable (like a list)
        vectorized_text = vectorizer.transform([cleaned_text])

        # 3. Predict using the model
        prediction = model.predict(vectorized_text)

        # prediction is likely an array, get the first element
        return prediction[0]
    except Exception as e:
        print(f"Error during prediction: {e}")
        return "Error during prediction"


# --- Training Function (Example - Run this separately if needed) ---
# You would typically run this in a separate script (e.g., train.py)
# or a Jupyter notebook, not directly within the API server process.

def train_and_save_model(data, labels):
    """Example function to train and save a simple model."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.pipeline import Pipeline

    print("Starting model training...")

    # Create a pipeline
    pipeline = Pipeline([
        ('vectorizer', TfidfVectorizer(stop_words='english', max_features=5000)),
        ('classifier', MultinomialNB())
    ])

    # Preprocess data (assuming 'data' is a list/Series of masked emails)
    cleaned_data = [clean_text_for_classification(text) for text in data]

    # Train the pipeline
    pipeline.fit(cleaned_data, labels)
    print("Model training complete.")

    # Save the pipeline components
    joblib.dump(pipeline.named_steps['classifier'], MODEL_PATH)
    joblib.dump(pipeline.named_steps['vectorizer'], VECTORIZER_PATH)
    print(f"Model saved to {MODEL_PATH}")
    print(f"Vectorizer saved to {VECTORIZER_PATH}")

# Example Usage (if you run this file directly for testing/training)
if __name__ == "__main__":
    # This block is for testing or initiating training manually.
    # Create dummy data for demonstration if needed:
    print("Running models.py directly...")
    dummy_emails = [
        "Subject: Billing Issue My account [full_name] was charged twice for order [order_id]. Please refund.",
        "Subject: Help needed Cannot login. My email is [email]. Reset password link broken.",
        "Subject: Account Management Request to close my account [account_num]. User [full_name]."
        ]
    dummy_labels = ["Billing Issues", "Technical Support", "Account Management"]

    # Uncomment to train a dummy model:
    # print("Training dummy model...")
    # train_and_save_model(dummy_emails, dummy_labels)
    # print("-" * 20)

    print("Attempting to load model and predict...")
    model, vectorizer = load_model_and_vectorizer()
    if model and vectorizer:
        test_email = "my login is not working help required email [email]"
        category = predict_category(test_email, model, vectorizer)
        print(f"Test Email: '{test_email}'")
        print(f"Predicted Category: {category}")
    else:
        print("Cannot perform prediction as model/vectorizer failed to load.")
