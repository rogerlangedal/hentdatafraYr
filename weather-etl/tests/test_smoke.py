import os

# Provide minimal env vars so Settings loads without needing a real .env file.
os.environ.setdefault("MET_USER_AGENT", "test-agent")
os.environ.setdefault("LOCATIONS", "Test:0:0:0")
os.environ.setdefault("DB_SERVER", "localhost,1433")
os.environ.setdefault("DB_DATABASE", "weather")

from weather_ingest.config import settings


def test_config_has_user_agent():
    assert settings.met_user_agent
