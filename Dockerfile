FROM python:3.11-slim

# metadane zgodne ze standardem OCI
LABEL org.opencontainers.image.authors="Paweł Ostrowski <s99649@pollub.edu.pl>"

# ustawienie katalogu roboczego
WORKDIR /app

# kopiowanie plików aplikacji do kontenera
COPY . .

# instalacja curl
RUN apt-get update && apt-get install -y curl && apt-get clean

# instalacja zależności
RUN pip install --no-cache-dir -r requirements.txt

# nasłuchiwanie na porcie 8000
EXPOSE 8000

# healthcheck
HEALTHCHECK --interval=10s --timeout=1s --retries=3 CMD curl -f http://localhost:8000/ || exit 1

# uruchomienie aplikacji
CMD ["python", "app.py"]
