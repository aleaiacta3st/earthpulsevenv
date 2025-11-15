# Use Python 3.11 slim image (smaller size)
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Copy requirements file first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose port 8000 for the API
EXPOSE 8000

# Command to run the API
CMD ["uvicorn", "alerts_api.main:app", "--host", "0.0.0.0", "--port", "8000"]