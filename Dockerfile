FROM python:3.11-slim

# Evita problemi di input interattivo
ENV PYTHONUNBUFFERED=1

# Installa dipendenze di sistema (solo se servono)
RUN apt-get update && apt-get install -y \
    build-essential \
    tk \
    && rm -rf /var/lib/apt/lists/*

# Crea la cartella dell'app
WORKDIR /app

# Copia i requisiti
COPY requirements.txt .

# Installa i pacchetti Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia il codice dell'app
COPY . .

# Comando di default
CMD ["python", "main.py"]