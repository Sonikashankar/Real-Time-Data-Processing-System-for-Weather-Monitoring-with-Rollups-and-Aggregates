# Dockerfile

# Use the official Python slim image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file to the working directory
COPY src/requirements.txt ./

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code to the working directory
COPY src/ ./

# Command to run the application
CMD ["python", "app.py"]
