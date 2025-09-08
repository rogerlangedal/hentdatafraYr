from weather_ingest.config import settings

def test_config_has_user_agent():
    assert settings.met_user_agent
