FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create directories for data persistence
RUN mkdir -p /app/data

# Set environment variable
ENV PYTHONUNBUFFERED=1

# Run the bot
CMD ["python", "main.py"]
