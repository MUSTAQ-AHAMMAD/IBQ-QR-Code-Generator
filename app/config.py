"""
Configuration management for IBQ QR Code Generator
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    app_name: str = "IBQ QR Code Generator"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    # QR Code
    default_qr_size: int = 10
    default_border: int = 4
    default_error_correction: str = "H"
    output_directory: str = "output"
    
    # Database
    database_url: str = "sqlite:///./qr_codes.db"
    
    # Cache
    enable_cache: bool = True
    cache_expiry_seconds: int = 3600
    
    # File Upload
    max_logo_size_mb: int = 5
    allowed_logo_formats: str = "png,jpg,jpeg"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
