# syntax=docker/dockerfile:1.6

FROM python:3.13-slim

LABEL org.opencontainers.image.authors="Paweł Ostrowski <s99649@pollub.edu.pl>"

WORKDIR /app

# Instalacja git i curl
RUN apt-get update && apt-get install -y git curl openssh-client && apt-get clean

# Dodanie github.com do zaufanych hostów ssh
RUN mkdir -p /root/.ssh && ssh-keyscan github.com >> /root/.ssh/known_hosts

# Pobranie kodu bezpośrednio z repozytorium GitHub
RUN --mount=type=ssh git clone git@github.com:Esco808/PAwChO_ZAD1.git /app

# Instalacja zależności
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=1s --retries=3 CMD curl -f http://localhost:8000/ || exit 1

CMD ["python", "app.py"]

