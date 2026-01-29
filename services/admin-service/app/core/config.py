from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    app_name: str = "Admin Service"
    debug: bool = False
    log_level: str = "INFO"
    
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

