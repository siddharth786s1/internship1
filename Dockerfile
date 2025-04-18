# filepath: Dockerfile
# Use an official Python runtime as a parent image (non-slim)
FROM python:3.9

# Set the working directory in the container
WORKDIR /code

# Install system dependencies needed for building Python packages
# (gcc/build-essential might already be in the non-slim image, but doesn't hurt)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /code
COPY requirements.txt .

# Install Python dependencies from requirements.txt first
# Ensure 'spacy' is listed in requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Separately install the specific spaCy model needed using pip and link it
RUN echo "Attempting to install and link spaCy model..." && \
    pip install --no-cache-dir https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl && \
    python -m spacy link en_core_web_sm en_core_web_sm && \
    echo "SpaCy model installed and linked successfully."

# Copy the rest of the application code into the container at /code
COPY . .

# Make port 7860 available (standard port for HF Spaces)
EXPOSE 7860

# Create the directory for saved models and set permissions
RUN mkdir -p saved_models && chmod 777 saved_models

# Command to run the application using Uvicorn, pointing to the 'app' instance in 'api.py'
# Bind to 0.0.0.0 and listen on port 7860
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "7860"]