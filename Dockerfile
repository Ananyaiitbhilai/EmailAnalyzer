# Use Python 3.10 base image
FROM python:3.10-slim

# Set working directory in container
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port 5000
EXPOSE 5000

# Start command with proper configuration for Render
CMD gunicorn --worker-class eventlet \
    --workers 1 \
    --bind 0.0.0.0:$PORT \
    --timeout 300 \
    --keep-alive 5 \
    --log-level info \
    --access-logfile - \
    --error-logfile - \
    --log-file - \
    app:app
