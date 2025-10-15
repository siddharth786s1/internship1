# Email Classification and PII Masking API

A privacy-first FastAPI service that masks Personally Identifiable Information (PII) from support emails and classifies the emails into predefined categories for automated triage. Built during my internship, the system combines rule-based regex + SpaCy NER for PII masking with a lightweight TF–IDF + Multinomial Naive Bayes classifier. The project is fully containerized with Docker for reproducible runs.

## Key features
- PII masking without LLMs: Regex patterns + SpaCy `en_core_web_sm` (PERSON)
- Email categorization: TF–IDF features + Multinomial Naive Bayes
- Simple HTTP API: FastAPI endpoint (`POST /classify/`)
- Reproducible environment: Docker image (Python 3.10) with pinned dependencies and bundled SpaCy model

## Project structure
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
└── .gitignore            # (Optional but recommended)
```

## Quickstart (local)
1) Create environment and install deps
```bash
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

2) Train (if no saved model exists)
```bash
# Make sure combined_emails_with_natural_pii.csv is in the repo root
python train.py
```

3) Run the API
```bash
python app.py
# or
uvicorn api:app --host 0.0.0.0 --port 8000
```
Visit http://127.0.0.1:8000

## Quickstart (Docker)
Build and run the containerized API.
```bash
docker build -t internship1:latest .
docker run --rm -p 8000:8000 internship1:latest
```
Then call the API at http://127.0.0.1:8000

## API usage
POST /classify/
- Request body
```json
{
  "email_body": "Hello, my name is Jane Doe and my card number is 4111-1111-1111-1111. My email is jane.doe@example.com. Please help with billing."
}
```

- Response (example)
```json
{
  "input_email_body": "Hello, my name is Jane Doe and my card number is 4111-1111-1111-1111. My email is jane.doe@example.com. Please help with billing.",
  "list_of_masked_entities": [
    {"position": [18, 26], "classification": "full_name", "entity": "Jane Doe"},
    {"position": [49, 68], "classification": "credit_debit_no", "entity": "4111-1111-1111-1111"},
    {"position": [83, 103], "classification": "email", "entity": "jane.doe@example.com"}
  ],
  "masked_email": "Hello, my name is [full_name] and my card number is [credit_debit_no]. My email is [email]. Please help with billing.",
  "category_of_the_email": "Billing Issues"
}
```

## Modeling details
- PII Masking: SpaCy `en_core_web_sm` for PERSON entities + curated regex for emails, phone numbers, credit/debit numbers, CVV, expiry, Aadhar, DOB, etc. Masking happens before feature extraction to avoid leakage.
- Classifier: Scikit-learn Pipeline with `TfidfVectorizer` feeding `MultinomialNB`.
- Artifact: `saved_models/email_classifier_pipeline.pkl` (loaded by `models.py`).
- Last observed training accuracy: ~69% (baseline to iterate on with more data/tuning).

## Design notes
- API: Implemented with FastAPI in `api.py`; server entry via `app.py` (Uvicorn).
- Reproducibility: Dockerfile pins Python 3.10, installs requirements, downloads SpaCy model at build time, and exposes port 8000.
- Security: The service returns masked text and entity spans to aid debugging without exposing raw PII in downstream systems.

## Roadmap / improvements
- Expand categories and rebalance training data
- Add robust validation (stratified splits, cross-validation) and track metrics beyond accuracy (F1/AUC)
- Experiment tracking (MLflow) and data versioning (DVC)
- Add unit tests for masking and inference; wire CI to build/test the Docker image
- Deploy to a managed environment (e.g., Hugging Face Spaces) and add link here

## Author
Built by Siddharth (@siddharth786s1) during internship.