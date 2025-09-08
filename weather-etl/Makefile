.PHONY: run build test fmt

run:
	python -m weather_ingest.main

build:
	docker build -f docker/Dockerfile -t weather-etl:local .

dev-up:
	docker compose -f docker/docker-compose.yml up --build

test:
	pytest -q

fmt:
	ruff check --fix . && black .
