from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    app_name: str = "Submission Service"
    debug: bool = False
    log_level: str = "INFO"
    
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    
    classification_service_url: str
    
    upload_dir: str = "./uploads"
    max_file_size: int = 10485760
    allowed_file_types: str = "image/jpeg,image/png,image/jpg"
    allowed_origins: str = "http://localhost:3000,http://localhost:8080"

    @property
    def allowed_file_types_list(self) -> List[str]:
        return [x.strip() for x in self.allowed_file_types.split(",") if x.strip()]

    @property
    def allowed_origins_list(self) -> List[str]:
        return [x.strip() for x in self.allowed_origins.split(",") if x.strip()]

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

