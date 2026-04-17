from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "SkinSenseAi"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "your_super_secret_key_please_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017" # Default, to be overridden by .env
    DATABASE_NAME: str = "skinsenseai_db"
    
    # External APIs
    GROQ_API_KEY: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
