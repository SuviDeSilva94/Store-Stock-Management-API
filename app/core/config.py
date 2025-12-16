from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Store Stock Management API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/storedb"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
