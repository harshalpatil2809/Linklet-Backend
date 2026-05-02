
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY start.sh /app/start.sh

RUN apt-get update && apt-get install -y dos2unix --no-install-recommends && \
    dos2unix /app/start.sh && \
    rm -rf /var/lib/apt/lists/*

RUN chmod +x /app/start.sh

EXPOSE 8000

CMD ["/app/start.sh"]