# platform-core/config/settings.py

from pydantic import BaseSettings

class AppSettings(BaseSettings):
    """
    Shared configuration model for tenant apps.
    """

    app_name: str = "insights-app"
    environment: str = "local"
    telemetry_enabled: bool = True

    class Config:
        env_prefix = "INSIGHTS_"
