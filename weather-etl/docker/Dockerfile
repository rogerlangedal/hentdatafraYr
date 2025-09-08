# Use the full Debian-based Python image to ensure apt-get is available
FROM python:3.11

# System deps + Microsoft repo for msodbcsql18
RUN apt-get update \
    && apt-get install -y curl gnupg apt-transport-https unixodbc-dev build-essential \
    && curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" \
       > /etc/apt/sources.list.d/microsoft.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app
COPY pyproject.toml /app/
RUN pip install --no-cache-dir -U pip && pip install --no-cache-dir .

COPY src/ /app/src/
ENV PYTHONPATH=/app/src

CMD ["python", "-m", "weather_ingest.main"]
