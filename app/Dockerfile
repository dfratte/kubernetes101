# Dockerfile for Kubernetes 101 Tutorial
# Builds a simple Python Flask web application

# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Copy templates directory
COPY templates/ ./templates/

# Set environment variables
ENV PORT=8080
ENV APP_VERSION=1.0.0

# Expose port 8080
EXPOSE 8080

# Run the application
CMD ["python", "app.py"]
