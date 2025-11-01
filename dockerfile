#  lightweight Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy dependency list first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose no ports (this is a background job)
# EXPOSE 8080 

# Load environment variables from .env at runtime using Docker's env options
# Command to run scheduler on container start
CMD ["python", "scheduler.py"]
