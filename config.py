"""Application configuration settings."""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings."""
    
    # MongoDB Configuration
    MONGO_URI: str = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    DB_NAME: str = "user_access_control"
    USERS_COLLECTION: str = "users"
    
    # API Configuration
    API_TITLE: str = "User Access Control API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Professional API for managing user access and authentication"
    
    # CORS Configuration (Security: Don't allow all origins in production)
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8080").split(",")
    CORS_ALLOW_CREDENTIALS: bool = False  # Set to True only if origins are specific
    CORS_ALLOW_METHODS: list = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    CORS_ALLOW_HEADERS: list = ["Content-Type", "Authorization"]
    
    # Password Configuration
    MIN_PASSWORD_LENGTH: int = 8
    REQUIRE_UPPERCASE: bool = True
    REQUIRE_DIGITS: bool = True
    REQUIRE_SPECIAL_CHARS: bool = True
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Security
    BCRYPT_ROUNDS: int = 12
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")


settings = Settings()
