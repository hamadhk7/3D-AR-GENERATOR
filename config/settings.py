"""
Application settings and configuration management.
"""

import os
from pathlib import Path
from typing import List, Optional
from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # API Configuration
    tripo_api_key: str = Field("demo_key", env="TRIPO_API_KEY")
    tripo_api_url: str = Field("https://api.tripo.ai", env="TRIPO_API_URL")
    
    # Server Configuration
    mcp_server_host: str = Field("localhost", env="MCP_SERVER_HOST")
    mcp_server_port: int = Field(8000, env="MCP_SERVER_PORT")
    web_server_host: str = Field("localhost", env="WEB_SERVER_HOST")
    web_server_port: int = Field(5000, env="WEB_SERVER_PORT")
    debug: bool = Field(False, env="DEBUG")
    
    # File Storage
    model_storage_path: Path = Field(Path("./data/generated_models"), env="MODEL_STORAGE_PATH")
    cache_path: Path = Field(Path("./data/cache"), env="CACHE_PATH")
    log_path: Path = Field(Path("./data/logs"), env="LOG_PATH")
    
    # Database
    database_url: str = Field("sqlite:///./data/app.db", env="DATABASE_URL")
    
    # Redis
    redis_url: str = Field("redis://localhost:6379/0", env="REDIS_URL")
    
    # Security
    secret_key: str = Field("demo_secret_key_change_in_production", env="SECRET_KEY")
    
    # Logging
    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_format: str = Field("json", env="LOG_FORMAT")
    
    # Model Generation
    default_model_quality: str = Field("high", env="DEFAULT_MODEL_QUALITY")
    default_model_format: str = Field("glb", env="DEFAULT_MODEL_FORMAT")
    max_generation_time: int = Field(300, env="MAX_GENERATION_TIME")
    max_file_size: str = Field("100MB", env="MAX_FILE_SIZE")
    
    # Rate Limiting
    rate_limit_requests: int = Field(100, env="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(3600, env="RATE_LIMIT_WINDOW")
    
    # CORS
    cors_origins: str = Field(
        "http://localhost:3000,http://localhost:5000",
        env="CORS_ORIGINS"
    )
    
    # Monitoring
    sentry_dsn: Optional[str] = Field(None, env="SENTRY_DSN")
    prometheus_enabled: bool = Field(True, env="PROMETHEUS_ENABLED")
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    @validator("model_storage_path", "cache_path", "log_path", pre=True)
    def create_directories(cls, v):
        """Create directories if they don't exist."""
        if isinstance(v, str):
            v = Path(v)
        v.mkdir(parents=True, exist_ok=True)
        return v
    
    @validator("max_file_size")
    def parse_file_size(cls, v):
        """Parse file size string to bytes."""
        if isinstance(v, str):
            v = v.upper()
            if v.endswith("KB"):
                return int(v[:-2]) * 1024
            elif v.endswith("MB"):
                return int(v[:-2]) * 1024 * 1024
            elif v.endswith("GB"):
                return int(v[:-2]) * 1024 * 1024 * 1024
            else:
                return int(v)
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings."""
    return settings


def validate_settings() -> None:
    """Validate all settings and create necessary directories."""
    # Validate API key
    if not settings.tripo_api_key:
        raise ValueError("TRIPO_API_KEY must be set in environment or .env file")
    
    # Validate secret key
    if not settings.secret_key:
        raise ValueError("SECRET_KEY must be set in environment or .env file")
    
    # Create necessary directories
    settings.model_storage_path.mkdir(parents=True, exist_ok=True)
    settings.cache_path.mkdir(parents=True, exist_ok=True)
    settings.log_path.mkdir(parents=True, exist_ok=True)
    
    # Create subdirectories
    (settings.model_storage_path / "glb").mkdir(exist_ok=True)
    (settings.model_storage_path / "usdz").mkdir(exist_ok=True)
    (settings.model_storage_path / "obj").mkdir(exist_ok=True)
    (settings.model_storage_path / "metadata").mkdir(exist_ok=True)
    (settings.cache_path / "downloads").mkdir(exist_ok=True)
    (settings.cache_path / "conversions").mkdir(exist_ok=True) 