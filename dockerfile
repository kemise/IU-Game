# Basis-Image festlegen
FROM python:3.9

# Arbeitsverzeichnis im Container erstellen
WORKDIR /app

# Abhängigkeiten installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Projektdateien in den Container kopieren
COPY . .

# Startbefehl definieren
CMD [ "python", "main.py" ]