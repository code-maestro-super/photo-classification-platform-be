from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    app_name: str = "Classification Service"
    debug: bool = False
    log_level: str = "INFO"
    
    allowed_origins: str = "http://localhost:3000,http://localhost:8080"

    @property
    def allowed_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

