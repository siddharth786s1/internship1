import pandas as pd
import requests
import json
from pathlib import Path
import time

# --- Configuration ---
DATASET_PATH = Path("combined_emails_with_natural_pii.csv") # Path to your input CSV
OUTPUT_PATH = Path("api_output_results.jsonl") # Where to save the results (JSON Lines format)
API_ENDPOINT = "http://127.0.0.1:8000/classify/" # Your running API endpoint

# Adjust column names if different
email_body_column = 'email'
# category_column = 'type' # Original category column (optional, for reference)

# --- Main Function ---
def process_emails_via_api(data_path: Path, output_path: Path, api_url: str):
    """
    Reads emails from a CSV, sends them to the classification API,
    and saves the JSON responses to a file.
    """
    if not data_path.exists():
        print(f"Error: Input dataset not found at {data_path}")
        return

    print(f"Loading dataset from {data_path}...")
    try:
        # Skip bad lines just in case, consistent with training
        df = pd.read_csv(data_path, on_bad_lines='skip')
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return

    if email_body_column not in df.columns:
        print(f"Error: Email body column '{email_body_column}' not found.")
        return

    # Handle potential missing email bodies
    df.dropna(subset=[email_body_column], inplace=True)
    if df.empty:
        print("Error: No valid email bodies found after handling missing values.")
        return

    results = []
    total_emails = len(df)
    print(f"Processing {total_emails} emails via API: {api_url}")

    # Open output file in write mode (clears existing content)
    with open(output_path, 'w') as f_out:
        for index, row in df.iterrows():
            email_text = str(row[email_body_column]) # Ensure it's a string
            payload = {"email_body": email_text}

            try:
                response = requests.post(api_url, json=payload, timeout=30) # Added timeout
                response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

                api_result = response.json()

                # Write result as a JSON line
                f_out.write(json.dumps(api_result) + '\n')

                if (index + 1) % 50 == 0: # Print progress every 50 emails
                    print(f"Processed {index + 1}/{total_emails} emails...")

            except requests.exceptions.RequestException as e:
                print(f"\nError processing email index {index}: {e}")
                # Optionally write error info to the file or a separate log
                error_info = {
                    "error": str(e),
                    "input_email_body": email_text,
                    "index": index
                }
                f_out.write(json.dumps(error_info) + '\n')
                # Optional: add a small delay if API is overloaded
                # time.sleep(0.5)
            except json.JSONDecodeError as e:
                 print(f"\nError decoding JSON response for email index {index}: {e}")
                 print(f"Response status code: {response.status_code}")
                 print(f"Response text: {response.text[:500]}...") # Print beginning of text
                 error_info = {
                    "error": f"JSONDecodeError: {e}",
                    "response_text": response.text,
                    "input_email_body": email_text,
                    "index": index
                 }
                 f_out.write(json.dumps(error_info) + '\n')


    print(f"\nProcessing complete. Results saved to {output_path}")


# --- Script Execution ---
if __name__ == "__main__":
    # Make sure the API is running before executing this script!
    print("--- Starting API Output Generation ---")
    print("Ensure the FastAPI server (python app.py or uvicorn) is running in another terminal.")
    input("Press Enter to continue once the API is running...")
    process_emails_via_api(DATASET_PATH, OUTPUT_PATH, API_ENDPOINT)
    print("--- Finished API Output Generation ---")
