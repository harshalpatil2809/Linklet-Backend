# 1. Base Image
FROM python:3.11-slim

# 2. Environment variables set karein
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Work directory set karein
WORKDIR /app

# 4. System dependencies install karein (PostgreSQL ke liye zaroori hai)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# 5. Requirements copy aur install karein
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# 6. Project files copy karein
COPY . /app/

# 7. Port expose karein
EXPOSE 8000

# 8. Server start karein
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]