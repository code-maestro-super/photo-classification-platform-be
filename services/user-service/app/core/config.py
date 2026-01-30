from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    app_name: str = "User Service"
    debug: bool = False
    log_level: str = "INFO"
    
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Comma-separated string from env; use .allowed_origins_list for CORS
    allowed_origins: str = "http://localhost:3000,http://localhost:8080"

    @property
    def allowed_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

