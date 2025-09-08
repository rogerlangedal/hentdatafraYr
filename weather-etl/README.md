# weather-etl

Minimal Python ETL that fetches weather forecasts from MET (api.met.no) and stores both raw JSON and flattened point data in SQL (Azure SQL-compatible). Local dev uses Docker Compose.

## Setup

### Docker
1. Copy env file:
   ```bash
   cp .env.example .env
   ```

   Set a strong `SA_PASSWORD` if you change it in compose.
2. Start services:

   ```bash
   docker compose -f docker/docker-compose.yml up --build
   ```

3. The app will create schema and fetch for the configured `LOCATIONS`. Check logs and connect to SQL on `localhost,1433` (db `weather`).

### WSL
Windows users can run the project inside [Windows Subsystem for Linux](https://learn.microsoft.com/windows/wsl/) (WSL 2).
From a WSL shell:

1. Create a virtual environment and install dependencies:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```

2. Copy env file and configure values:

   ```bash
   cp .env.example .env
   ```

3. Run the ETL or other Makefile tasks:

   ```bash
   python -m weather_ingest.main
   ```

Docker Desktop with the WSL 2 backend is also supported; follow the Docker steps above within your WSL environment.

## Notes

* **User-Agent** must identify your app + contact per MET terms.
* The client uses `If-Modified-Since` to reduce calls; respect rate limits.
* In Azure, prefer passwordless with Managed Identity (set `USE_MI=true`).

## Tests

```bash
pytest -q
```

## Development

Format and test the code before committing:

```bash
make fmt
make test
```

The repository includes VS Code tasks for these commands. Open the command
palette and run **Tasks: Run Task** to execute them.

## CI

GitHub Actions runs linting and tests on each push and pull request. The
workflow definition lives in `.github/workflows/ci.yml`.
