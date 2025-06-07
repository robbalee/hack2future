"""
Environment-based configuration for the Insurance Fraud Detection System.
Provides different configurations for development, staging, and production environments.
"""
import os
from abc import ABC, abstractmethod


class BaseConfig(ABC):
    """Base configuration class with common settings"""
    
    # Application Settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = False
    TESTING = False
    
    # File Upload Settings
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    
    # Storage Settings
    CLAIMS_DIR = 'claims_data'
    EVENTS_DIR = 'events_data'
    BACKUP_DIR = 'backups'
    
    # Cosmos DB Settings
    COSMOS_DATABASE = os.environ.get('COSMOS_DATABASE', 'insurance-claims-db')
    COSMOS_CLAIMS_CONTAINER = os.environ.get('COSMOS_CLAIMS_CONTAINER', 'claims')
    COSMOS_EVENTS_CONTAINER = os.environ.get('COSMOS_EVENTS_CONTAINER', 'events')
    
    @abstractmethod
    def validate(self):
        """Validate configuration for environment"""
        pass


class DevelopmentConfig(BaseConfig):
    """Configuration for local development environment"""
    
    DEBUG = True
    
    # Cosmos DB - Optional for development
    COSMOS_ENDPOINT = os.environ.get('COSMOS_ENDPOINT', '')
    COSMOS_KEY = os.environ.get('COSMOS_KEY', '')
    USE_COSMOS = bool(COSMOS_ENDPOINT and COSMOS_KEY)
    USE_MANAGED_IDENTITY = False
    FALLBACK_TO_LOCAL = True
    
    # Logging
    LOG_LEVEL = 'DEBUG'
    
    def validate(self):
        """Development config is always valid - can work without Cosmos"""
        if self.USE_COSMOS and not self.COSMOS_ENDPOINT:
            raise ValueError("COSMOS_ENDPOINT required when USE_COSMOS is True")
        return True


class StagingConfig(BaseConfig):
    """Configuration for staging environment"""
    
    DEBUG = False
    
    # Cosmos DB - Required for staging
    COSMOS_ENDPOINT = os.environ.get('COSMOS_ENDPOINT')
    USE_MANAGED_IDENTITY = os.environ.get('USE_MANAGED_IDENTITY', 'false').lower() == 'true'
    USE_COSMOS = True
    FALLBACK_TO_LOCAL = True  # Still allow fallback in staging
    
    # Authentication
    COSMOS_KEY = os.environ.get('COSMOS_KEY', '') if not USE_MANAGED_IDENTITY else None
    
    # Logging
    LOG_LEVEL = 'INFO'
    
    def validate(self):
        """Staging requires Cosmos endpoint"""
        if not self.COSMOS_ENDPOINT:
            raise ValueError("COSMOS_ENDPOINT is required for staging environment")
        
        if not self.USE_MANAGED_IDENTITY and not self.COSMOS_KEY:
            raise ValueError("COSMOS_KEY required when not using managed identity")
        
        return True


class ProductionConfig(BaseConfig):
    """Configuration for production environment"""
    
    DEBUG = False
    
    # Cosmos DB - Required and must use Managed Identity
    COSMOS_ENDPOINT = os.environ.get('COSMOS_ENDPOINT')
    USE_MANAGED_IDENTITY = True
    USE_COSMOS = True
    FALLBACK_TO_LOCAL = False  # Fail if Cosmos unavailable in production
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Logging
    LOG_LEVEL = 'WARNING'
    
    # Application Insights
    APPLICATIONINSIGHTS_CONNECTION_STRING = os.environ.get('APPLICATIONINSIGHTS_CONNECTION_STRING')
    
    def validate(self):
        """Production has strict requirements"""
        if not self.COSMOS_ENDPOINT:
            raise ValueError("COSMOS_ENDPOINT is required for production")
        
        if not self.SECRET_KEY or self.SECRET_KEY == 'dev-secret-key-change-in-production':
            raise ValueError("Proper SECRET_KEY is required for production")
        
        return True


class ConfigFactory:
    """Factory for creating configuration objects based on environment"""
    
    @staticmethod
    def create_config():
        """Create configuration based on FLASK_ENV environment variable"""
        env = os.environ.get('FLASK_ENV', 'development').lower()
        
        config_map = {
            'development': DevelopmentConfig,
            'staging': StagingConfig,
            'production': ProductionConfig
        }
        
        config_class = config_map.get(env, DevelopmentConfig)
        config = config_class()
        
        # Validate configuration
        config.validate()
        
        return config


# Convenience function for backwards compatibility
def get_config():
    """Get configuration for current environment"""
    return ConfigFactory.create_config()
