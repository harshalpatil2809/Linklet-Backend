
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    dos2unix \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the backend project
COPY . /app/

# Normalize start.sh line endings and make it executable
COPY start.sh /app/start.sh

RUN dos2unix /app/start.sh && \
    chmod +x /app/start.sh

EXPOSE 8000

# Start the application using start.sh
CMD ["sh", "/app/start.sh"]
