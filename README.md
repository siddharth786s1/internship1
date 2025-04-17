# Email Classification and PII Masking API

This project implements an API to classify support emails into predefined categories while masking Personally Identifiable Information (PII) before processing.

## Project Structure

```
.
├── api.py             # FastAPI application logic
├── models.py          # Model loading, prediction (and optional training) logic
├── utils.py           # PII masking and text utility functions
├── requirements.txt   # Python dependencies
├── saved_models/      # Directory for trained models (classifier, vectorizer)
├── data/              # Directory for datasets (add your data here)
├── .env               # (Optional) For environment variables
├── .gitignore         # Git ignore file
└── README.md          # This file
```

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-name>
    ```

2.  **Create and activate a virtual environment:** (Recommended)
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Download NLP models:**
    ```bash
    python -m spacy download en_core_web_sm
    # Run inside python interpreter if needed:
    # import nltk; nltk.download('punkt'); nltk.download('stopwords')
    ```

5.  **(Crucial Step) Train the Model:**
    *   You need to train the classification model first. Add your training data to the `data/` directory.
    *   Adapt and run the training logic (e.g., the `train_and_save_model` function in `models.py`, potentially moving it to a separate `train.py` script). This will create the necessary files in `saved_models/`.
    *   Example (modify as needed): `python models.py` (if you add training execution there) or `python train.py`

## Running the API Locally

Once the models are trained and saved:

```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000` (or the port forwarded by your Codespace).

## API Usage

Send a POST request to the `/classify/` endpoint with a JSON body containing the email text:

**Endpoint:** `POST /classify/`

**Request Body:**

```json
{
  "email_body": "Your email content here. My name is John Smith and my number is 555-123-4567."
}
```

**Example Response:**

```json
{
  "input_email_body": "Your email content here. My name is John Smith and my number is 555-123-4567.",
  "list_of_masked_entities": [
    {
      "position": [34, 44],
      "classification": "full_name",
      "entity": "John Smith"
    },
    {
      "position": [61, 73],
      "classification": "phone_number",
      "entity": "555-123-4567"
    }
  ],
  "masked_email": "Your email content here. My name is [full_name] and my number is [phone_number].",
  "category_of_the_email": "Predicted Category" // e.g., "Account Management"
}
```

## Deployment

(Add instructions for deploying to Hugging Face Spaces later)

## Report

(Link to or include your report here)