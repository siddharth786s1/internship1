# filepath: /workspaces/internship1/train.py
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from pathlib import Path

# --- Local Imports ---
# Ensure utils.py has the clean_text_for_classification function
try:
    from utils import clean_text_for_classification
except ImportError:
    print("Error: Could not import clean_text_for_classification from utils.")
    print("Make sure utils.py exists and the function is defined.")
    # Define a basic fallback if needed for testing, but fix the import
    def clean_text_for_classification(text: str) -> str:
        return text.lower().strip()

# --- Configuration ---
# !! ADJUST THESE PATHS AND COLUMN NAMES !!
DATASET_PATH = Path("combined_emails_with_natural_pii.csv")
MODEL_DIR = Path("saved_models")
MODEL_PATH = MODEL_DIR / "email_classifier_pipeline.pkl"
email_body_column = 'email'      # <<< Ensure this is 'email'
category_column = 'type'         # <<< Ensure this is 'type'

# --- Main Training Function ---
def train_model(data_path: Path, model_save_path: Path):
    """Loads data, trains the model pipeline, and saves it."""

    if not data_path.exists():
        print(f"Error: Dataset not found at {data_path}")
        print("Please make sure the CSV file is uploaded to your Codespace.")
        return

    print(f"Loading dataset from {data_path}...")
    try:
        # Keep the on_bad_lines='skip' if it worked
        df = pd.read_csv(data_path, engine='python', on_bad_lines='skip')
        print(f"Dataset loaded. Note: Bad lines may have been skipped.")
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return

    # --- Data Validation ---
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


# --- Script Execution ---
if __name__ == "__main__":
    # Make sure the MODEL_DIR exists before calling train_model if needed elsewhere
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    train_model(DATASET_PATH, MODEL_PATH)