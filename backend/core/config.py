from typing import List
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    VERSION: str = "1.0.0"
    APP_NAME: str = "Nexus Trading Terminal"
    ENV: str = "development"
    DEBUG: bool = True
    
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    DATABASE_URL: str
    REDIS_URL: str
    
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    POLYGON_API_KEY: str = ""
    ALPACA_API_KEY: str = ""
    ALPACA_SECRET_KEY: str = ""
    IB_HOST: str = "127.0.0.1"
    IB_PORT: int = 7497
    BINANCE_API_KEY: str = ""
    BINANCE_SECRET: str = ""
    
    ETHEREUM_RPC: str = ""
    SOLANA_RPC: str = ""
    
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    
    NEWS_API_KEY: str = ""
    TWITTER_BEARER_TOKEN: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
