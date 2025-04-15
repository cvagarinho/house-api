FROM python:3.12.2-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variable
ENV RUN_MODE=api

# Use direct command instead of entrypoint script
CMD [ "sh", "-c", "if [ \"$RUN_MODE\" = \"worker\" ]; then python -m app.workers.recommendation_worker; else uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload; fi" ]