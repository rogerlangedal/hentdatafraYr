from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # MET / api.met.no
    met_user_agent: str = Field(..., alias="MET_USER_AGENT")  # e.g., "your-app/0.1 you@company.no"
    # Comma-separated list: name:lat:lon:alt
    locations: str = Field(..., alias="LOCATIONS")

    # Database (local uses username/password; Azure uses managed identity)
    db_server: str = Field(..., alias="DB_SERVER")  # "localhost,1433" or "<server>.database.windows.net"
    db_database: str = Field(..., alias="DB_DATABASE")
    db_user: str | None = Field(None, alias="DB_USER")
    db_password: str | None = Field(None, alias="DB_PASSWORD")
    use_managed_identity: bool = Field(False, alias="USE_MI")

    schedule_cron: str = Field("*/30 * * * *", alias="SCHEDULE_CRON")  # every 30 minutes

    model_config = {"env_file": ".env", "extra": "ignore"}

settings = Settings()
