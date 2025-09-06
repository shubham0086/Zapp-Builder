from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Content Creator Studio"
    VERSION: str = "0.1.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str = "sqlite:///./content_studio.db"
    REDIS_URL: str = "redis://localhost:6379"
    
    # LLM APIs
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""
    
    # External APIs
    SERP_API_KEY: str = ""
    SOCIAL_MEDIA_API_KEY: str = ""
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Rate Limiting
    REQUESTS_PER_MINUTE: int = 100
    REQUESTS_PER_HOUR: int = 1000
    
    # Agent Settings
    MAX_RESEARCH_SOURCES: int = 10
    MAX_LEAD_RESULTS: int = 50
    CONTENT_GENERATION_TIMEOUT: int = 120
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()