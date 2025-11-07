"""
Application Configuration using Pydantic V2 Settings
Supports environment variables and .env files
"""

from typing import List, Optional, Any
from pydantic import (
    BaseModel,
    Field,
    PostgresDsn,
    field_validator,
    ConfigDict,
    ValidationInfo,
)
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import secrets


# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class DatabaseSettings(BaseModel):
    """PostgreSQL Database Settings"""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
    )
    
    type: str = Field(default="postgresql", description="Database type")
    driver: str = Field(default="postgresql+psycopg2", description="Database driver")
    async_driver: str = Field(default="postgresql+asyncpg", description="Async driver")
    host: str = Field(default="localhost", description="Database host")
    port: int = Field(default=5432, ge=1, le=65535, description="Database port")
    name: str = Field(default="hospital_db", description="Database name")
    user: str = Field(default="postgres", description="Database user")
    password: str = Field(default="postgres", description="Database password")
    schema: str = Field(default="public", description="Database schema")
    
    # Connection Pool Settings
    pool_size: int = Field(default=20, ge=5, le=100)
    max_overflow: int = Field(default=10, ge=0, le=50)
    pool_timeout: int = Field(default=30, ge=5, le=300)
    pool_recycle: int = Field(default=3600, ge=300)
    pool_pre_ping: bool = Field(default=True)
    
    # Query Settings
    echo: bool = Field(default=False, description="Echo SQL queries")
    echo_pool: bool = Field(default=False)
    statement_timeout: int = Field(default=30000, description="Statement timeout in ms")
    
    @property
    def url(self) -> str:
        """Synchronous database URL"""
        return f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
    
    @property
    def async_url(self) -> str:
        """Asynchronous database URL"""
        return f"{self.async_driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class RedisSettings(BaseModel):
    """Redis Cache Settings"""
    
    model_config = ConfigDict(validate_assignment=True)
    
    enabled: bool = Field(default=True)
    host: str = Field(default="localhost")
    port: int = Field(default=6379, ge=1, le=65535)
    db: int = Field(default=0, ge=0, le=15)
    password: Optional[str] = Field(default=None)
    cache_expire: int = Field(default=3600, ge=60)
    max_connections: int = Field(default=50, ge=10, le=200)
    socket_timeout: int = Field(default=5)
    
    @property
    def url(self) -> str:
        """Redis connection URL"""
        if self.password:
            return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"
        return f"redis://{self.host}:{self.port}/{self.db}"


class CelerySettings(BaseModel):
    """Celery Background Task Settings"""
    
    model_config = ConfigDict(validate_assignment=True)
    
    broker_url: str = Field(default="redis://localhost:6379/0")
    result_backend: str = Field(default="redis://localhost:6379/0")
    task_serializer: str = Field(default="json")
    result_serializer: str = Field(default="json")
    accept_content: List[str] = Field(default=["json", "application/json"])
    timezone: str = Field(default="UTC")
    enable_utc: bool = Field(default=True)
    task_track_started: bool = Field(default=True)
    task_time_limit: int = Field(default=300)
    task_soft_time_limit: int = Field(default=240)


class SecuritySettings(BaseModel):
    """Security & Authentication Settings"""
    
    model_config = ConfigDict(validate_assignment=True)
    
    secret_key: str = Field(
        default_factory=lambda: secrets.token_urlsafe(32),
        min_length=32,
        description="Secret key for JWT"
    )
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30, ge=5, le=1440)
    refresh_token_expire_days: int = Field(default=7, ge=1, le=30)
    
    # Password Settings
    password_hash_algorithm: str = Field(default="argon2")
    password_bcrypt_rounds: int = Field(default=12, ge=10, le=16)
    password_min_length: int = Field(default=8, ge=6, le=128)
    password_require_uppercase: bool = Field(default=True)
    password_require_lowercase: bool = Field(default=True)
    password_require_digit: bool = Field(default=True)
    password_require_special: bool = Field(default=True)


class CORSSettings(BaseModel):
    """CORS Configuration"""
    
    model_config = ConfigDict(validate_assignment=True)
    
    origins: List[str] = Field(
        default=[
            "http://localhost:3000",
            "http://localhost:8000",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:8000",
        ]
    )
    credentials: bool = Field(default=True)
    methods: List[str] = Field(default=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
    headers: List[str] = Field(default=["*"])
    max_age: int = Field(default=3600)


class EmailSettings(BaseModel):
    """SMTP Email Settings"""
    
    model_config = ConfigDict(validate_assignment=True)
    
    enabled: bool = Field(default=True)
    host: str = Field(default="smtp.gmail.com")
    port: int = Field(default=587, ge=1, le=65535)
    username: str = Field(default="")
    password: str = Field(default="")
    from_email: str = Field(default="noreply@hospital.com")
    from_name: str = Field(default="Hospital Management System")
    tls: bool = Field(default=True)
    ssl: bool = Field(default=False)
    timeout: int = Field(default=60)


class FileUploadSettings(BaseModel):
    """File Upload Configuration"""
    
    model_config = ConfigDict(validate_assignment=True)
    
    max_upload_size: int = Field(default=10485760, description="10MB in bytes")
    max_upload_size_mb: int = Field(default=10)
    allowed_image_extensions: List[str] = Field(
        default=[".jpg", ".jpeg", ".png", ".gif", ".webp"]
    )
    allowed_document_extensions: List[str] = Field(
        default=[".pdf", ".doc", ".docx", ".xls", ".xlsx", ".txt", ".csv"]
    )
    upload_dir: Path = Field(default=BASE_DIR / "uploads")
    static_dir: Path = Field(default=BASE_DIR / "static")
    temp_dir: Path = Field(default=BASE_DIR / "temp")


class LoggingSettings(BaseModel):
    """Logging Configuration"""
    
    model_config = ConfigDict(validate_assignment=True)
    
    level: str = Field(default="INFO")
    format: str = Field(default="json")
    file: Path = Field(default=BASE_DIR / "logs" / "app.log")
    max_size: int = Field(default=10485760, description="10MB")
    backup_count: int = Field(default=5)
    rotation: str = Field(default="10 MB")
    retention: str = Field(default="30 days")


class Settings(BaseSettings):
    """
    Main Application Settings using Pydantic V2
    Loads from environment variables and .env file
    """
    
    # Pydantic V2 Settings Configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        validate_assignment=True,
        str_strip_whitespace=True,
    )
    
    # Application Info
    app_name: str = Field(default="Hospital Management System")
    app_version: str = Field(default="1.0.0")
    app_description: str = Field(
        default="Comprehensive Hospital Management System API with Pydantic V2"
    )
    environment: str = Field(default="development")
    debug: bool = Field(default=True)
    api_prefix: str = Field(default="/api/v1")
    
    # Server Settings
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000, ge=1, le=65535)
    reload: bool = Field(default=True)
    workers: int = Field(default=4, ge=1, le=16)
    
    # Nested Settings (Pydantic V2 way)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    celery: CelerySettings = Field(default_factory=CelerySettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    cors: CORSSettings = Field(default_factory=CORSSettings)
    email: EmailSettings = Field(default_factory=EmailSettings)
    file_upload: FileUploadSettings = Field(default_factory=FileUploadSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    
    # Pagination
    default_page_size: int = Field(default=20, ge=1, le=100)
    max_page_size: int = Field(default=100, ge=10, le=1000)
    
    # Rate Limiting
    rate_limit_enabled: bool = Field(default=True)
    rate_limit_per_minute: int = Field(default=60)
    rate_limit_per_hour: int = Field(default=1000)
    
    # Floor Settings (Hospital Specific)
    max_floors: int = Field(default=50, ge=1, le=200)
    max_basement_floors: int = Field(default=5, ge=0, le=10)
    min_floor_number: int = Field(default=-5)
    ground_floor_number: int = Field(default=0)
    
    # Feature Flags
    enable_appointments: bool = Field(default=True)
    enable_lab_tests: bool = Field(default=True)
    enable_pharmacy: bool = Field(default=True)
    enable_billing: bool = Field(default=True)
    
    # API Documentation
    docs_url: str = Field(default="/docs")
    redoc_url: str = Field(default="/redoc")
    openapi_url: str = Field(default="/openapi.json")
    enable_docs: bool = Field(default=True)
    
    # Testing
    testing: bool = Field(default=False)
    test_database_url: Optional[str] = Field(default=None)
    
    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment value"""
        allowed = ["development", "staging", "production", "testing"]
        if v.lower() not in allowed:
            raise ValueError(f"Environment must be one of: {', '.join(allowed)}")
        return v.lower()
    
    @field_validator("api_prefix")
    @classmethod
    def validate_api_prefix(cls, v: str) -> str:
        """Ensure API prefix starts with /"""
        if not v.startswith("/"):
            return f"/{v}"
        return v
    
    def __init__(self, **kwargs):
        """Initialize settings and create directories"""
        super().__init__(**kwargs)
        self._create_directories()
    
    def _create_directories(self) -> None:
        """Create necessary directories if they don't exist"""
        dirs = [
            self.file_upload.upload_dir,
            self.file_upload.static_dir,
            self.file_upload.temp_dir,
            self.logging.file.parent,
        ]
        for directory in dirs:
            directory.mkdir(parents=True, exist_ok=True)
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.environment == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.environment == "production"
    
    @property
    def database_url(self) -> str:
        """Get database URL"""
        if self.testing and self.test_database_url:
            return self.test_database_url
        return self.database.url
    
    @property
    def async_database_url(self) -> str:
        """Get async database URL"""
        return self.database.async_url
    
    class Config:
        """Pydantic V1 compatibility (if needed)"""
        case_sensitive = False


# Create settings instance
settings = Settings()


# Export for convenience
__all__ = [
    "settings",
    "Settings",
    "DatabaseSettings",
    "RedisSettings",
    "SecuritySettings",
    "CORSSettings",
    "EmailSettings",
    "FileUploadSettings",
    "LoggingSettings",
]