# Dockerfile (in ~/Desktop/iwProject)

FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

# Installeer Python + venv-ondersteuning
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv && \
    rm -rf /var/lib/apt/lists/*

# Maak de venv
WORKDIR /app
RUN python3 -m venv venv

# Zorg dat we pip in de venv gebruiken
ENV PATH="/app/venv/bin:$PATH"

# Kopieer requirements en installeer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopieer de webapp
COPY webapp/ ./webapp

# Expose poort
EXPOSE 5000

# Start de Flask-app (gebruikt nu de venv-python)
CMD ["python3", "webapp/app.py"]
