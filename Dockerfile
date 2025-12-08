FROM python:3.11-slim

# Avoid buffering issues
ENV PYTHONUNBUFFERED=1

# Install system dependencies for WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    tk \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz0b \
    libharfbuzz-subset0 \
    libjpeg-dev \
    libopenjp2-7-dev \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Create app folder
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Default command
CMD ["python", "main.py"]
