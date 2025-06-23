# Use official Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements.txt first (for better Docker caching if you update code)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose port
EXPOSE 8000

# Healthcheck for Docker
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
 CMD curl --fail http://localhost:8000/health || exit 1

# Run the FastAPI app using uvicorn
CMD ["uvicorn", "fuzzy_search_service:app", "--host", "0.0.0.0", "--port", "8000"]

