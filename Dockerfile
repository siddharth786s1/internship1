# filepath: Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container at /code
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Use --no-cache-dir to reduce image size
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /code
COPY . .

# Make port 7860 available to the world outside this container
# Hugging Face Spaces expects the app to listen on port 7860 by default
EXPOSE 7860

# Define environment variable for the port (optional, Uvicorn uses --port)
# ENV PORT=7860 # Not strictly needed if passed in CMD

# Command to run the application using Uvicorn
# It needs to bind to 0.0.0.0 to be accessible from outside the container.
# It should listen on port 7860 as expected by Spaces.
# Use api:app to tell Uvicorn where to find the FastAPI instance ('app' object inside 'api.py')
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "7860"]