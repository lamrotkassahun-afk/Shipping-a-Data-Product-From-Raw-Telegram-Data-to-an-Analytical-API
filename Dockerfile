# Use a lightweight Python base image
FROM python:3.11-slim

# Install system dependencies for PostgreSQL and OpenCV (needed for YOLO)
# Install system dependencies for PostgreSQL and OpenCV (needed for YOLO)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the API
# This ensures python looks in its site-packages for the uvicorn module
CMD ["python", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]