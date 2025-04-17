# Email Classification and PII Masking API

This project implements an API service for classifying support emails into predefined categories while masking Personally Identifiable Information (PII) before classification.

## Objective

To build an email classification system for a support team that:
1.  Masks PII (Full Name, Email, Phone, DOB, Aadhar, Card Numbers, CVV, Expiry) using Regex and SpaCy NER (without LLMs).
2.  Classifies emails into categories (e.g., Billing Issues, Technical Support) using a trained machine learning model.
3.  Exposes this functionality via a FastAPI endpoint.

## Project Structure

```
/workspaces/internship1/
├── saved_models/
│   └── email_classifier_pipeline.pkl   # Saved classification model pipeline
├── api.py                # FastAPI application logic and endpoints
├── app.py                # Script to run the Uvicorn server
├── models.py             # Model loading, prediction functions
├── utils.py              # PII masking logic, text cleaning
├── train.py              # Script to train the classification model
├── requirements.txt      # Python package dependencies
├── combined_emails_with_natural_pii.csv # Dataset used for training (ensure this is present)
├── README.md             # This file
└── .gitignore            # (Optional but recommended: add *.pyc, __pycache__, .venv, saved_models/*, *.csv)
```

## Setup

1.  **Clone the repository (if applicable):**
    ```bash
    git clone <your-repo-url>
    cd internship1
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    # On Windows use: .venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Download SpaCy Model (if not done automatically by `utils.py`):**
    ```bash
    python -m spacy download en_core_web_sm
    ```
5.  **Train the Model (if `saved_models/email_classifier_pipeline.pkl` is not present):**
    *   Ensure the dataset (`combined_emails_with_natural_pii.csv`) is in the root directory.
    *   Run the training script:
        ```bash
        python train.py
        ```

## Running the API

1.  **Start the FastAPI server:**
    ```bash
    python app.py
    # OR directly using uvicorn:
    # uvicorn api:app --host 0.0.0.0 --port 8000 --reload
    ```
    The API will be available at `http://127.0.0.1:8000` (or the port specified).

## Using the API

Send a POST request to the `/classify/` endpoint with a JSON body containing the email text.

**Example using `curl`:**

```bash
curl -X POST "http://127.0.0.1:8000/classify/" \
     -H "Content-Type: application/json" \
     -d '{
           "email_body": "Hello, my name is Jane Doe and my card number is 4111-1111-1111-1111. My email is jane.doe@example.com. Please help with billing."
         }'
```

**Expected Response Structure:**

```json
{
  "input_email_body": "Hello, my name is Jane Doe and my card number is 4111-1111-1111-1111. My email is jane.doe@example.com. Please help with billing.",
  "list_of_masked_entities": [
    {
      "position": [18, 26],
      "classification": "full_name",
      "entity": "Jane Doe"
    },
    {
      "position": [49, 68],
      "classification": "credit_debit_no",
      "entity": "4111-1111-1111-1111"
    },
    {
      "position": [83, 103],
      "classification": "email",
      "entity": "jane.doe@example.com"
    }
  ],
  "masked_email": "Hello, my name is [full_name] and my card number is [credit_debit_no]. My email is [email]. Please help with billing.",
  "category_of_the_email": "Billing Issues" // Example category
}
```

## Model Details

*   **PII Masking:** SpaCy (`en_core_web_sm` for PERSON) and custom Regex patterns.
*   **Classification Model:** TF-IDF Vectorizer + Multinomial Naive Bayes.
*   **Training Accuracy:** Approx. 69% (as per last training run).

## Deployment

(Add link to your Hugging Face Space deployment here once completed)

```
HF Space: [Link]
```