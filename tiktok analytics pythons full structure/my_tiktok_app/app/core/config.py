from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "TikTok Analytics + RAG Chatbot"
    DEBUG: bool = True
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/tiktok_analytics"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # OpenAI
    OPENAI_API_KEY: str = "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"
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    
    # Vector Database
    VECTOR_DB_TYPE: str = "chroma"  # or "pinecone"
    CHROMA_PERSIST_DIRECTORY: str = "./chroma_db"
    PINECONE_API_KEY: Optional[str] = None
    PINECONE_ENVIRONMENT: Optional[str] = None
    PINECONE_INDEX_NAME: str = "tiktok-knowledge-base"
    
    # TikTok API (dummy for now)
    TIKTOK_API_KEY: str = "dummy-tiktok-api-key"
    TIKTOK_API_SECRET: str = "dummy-tiktok-api-secret"
    
    # JWT
    JWT_SECRET_KEY: str = "your-jwt-secret-key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    class Config:
        env_file = ".env"

settings = Settings() 