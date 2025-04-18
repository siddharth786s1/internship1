# filepath: Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /code

# Install system dependencies needed for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /code
COPY requirements.txt .

# Install Python dependencies
# Use --no-cache-dir to reduce image size
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /code
COPY . .

# Make port 7860 available (standard port for HF Spaces)
EXPOSE 7860

# Command to run the application using Uvicorn, pointing to the 'app' instance in 'api.py'
# Bind to 0.0.0.0 and listen on port 7860
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "7860"]