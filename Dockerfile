# Use an official Python runtime as a parent image
# Using a specific version like 3.10 is recommended for stability
FROM python:3.10

# Set environment variables
# Prevents Python from writing pyc files to disc (optional)
ENV PYTHONDONTWRITEBYTECODE 1
# Ensures Python output is sent straight to terminal (useful for logs)
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies if any (unlikely needed for this setup)
# RUN apt-get update && apt-get install -y --no-install-recommends some-package && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir reduces image size
# --upgrade pip ensures the latest pip is used
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Download the spaCy model
# This ensures the model is part of the image and doesn't need downloading at runtime
RUN python -m spacy download en_core_web_sm

# Copy the rest of the application code into the working directory
# This includes api.py, utils.py, models.py, and the saved_models directory
COPY . .

# Expose the port the app runs on (default for uvicorn is 8000)
EXPOSE 8000

# Define the command to run the application
# Use 0.0.0.0 to make it accessible from outside the container
# --reload is useful for development but should be removed for production images
# CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# Use this CMD for production/deployment on Hugging Face Spaces:
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]