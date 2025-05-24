"""
Enhanced configuration management for Financial Risk Assessment System
Supports multiple environments and configuration sources
"""
import os
import yaml
from dotenv import load_dotenv
from typing import Dict, Any
import logging

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class with common settings"""
    
    # Application metadata
    APP_TITLE = os.getenv('APP_TITLE', 'Financial Risk Assessment System')
    APP_VERSION = os.getenv('APP_VERSION', '2.0.0')
    APP_DESCRIPTION = 'Professional Financial Risk Assessment and Management System'
    
    # Database configuration
    DB_TYPE = os.getenv('DB_TYPE', 'sqlite')  # 'sqlite' or 'postgres'
    DB_NAME = os.getenv('DB_NAME', 'user_management.db')
    
    # PostgreSQL configuration (for production)
    PG_HOST = os.getenv('PG_HOST', 'localhost')
    PG_PORT = int(os.getenv('PG_PORT', 5432))
    PG_DATABASE = os.getenv('PG_DATABASE', 'risk_control')
    PG_USER = os.getenv('PG_USER', 'postgres')
    PG_PASSWORD = os.getenv('PG_PASSWORD', 'postgres')
    PG_SSLMODE = os.getenv('PG_SSLMODE', 'prefer')
    
    # Connection pool settings
    MAX_POOL_SIZE = int(os.getenv('MAX_POOL_SIZE', 5))
    POOL_TIMEOUT = int(os.getenv('POOL_TIMEOUT', 30))
    
    # Window size defaults
    LOGIN_WINDOW_SIZE = (350, 250)
    USER_INFO_WINDOW_SIZE = (600, 500)
    ADMIN_WINDOW_SIZE = (1200, 800)
    
    # System roles and permissions
    ROLES = {
        'ADMIN': 1,
        'USER': 0,
        'RISK_ANALYST': 2,
        'COMPLIANCE_OFFICER': 3
    }
    
    # Permission levels
    PERMISSIONS = {
        'READ': 1,
        'WRITE': 2,
        'DELETE': 4,
        'ADMIN': 8
    }
    
    # Security settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    PASSWORD_MIN_LENGTH = int(os.getenv('PASSWORD_MIN_LENGTH', 8))
    SESSION_TIMEOUT = int(os.getenv('SESSION_TIMEOUT', 3600))  # seconds
    MAX_LOGIN_ATTEMPTS = int(os.getenv('MAX_LOGIN_ATTEMPTS', 3))
    
    # Logging configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'financial_risk_system.log')
    LOG_MAX_SIZE = int(os.getenv('LOG_MAX_SIZE', 10485760))  # 10MB
    LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', 5))
    
    # Risk assessment settings
    RISK_THRESHOLD_LOW = float(os.getenv('RISK_THRESHOLD_LOW', 0.3))
    RISK_THRESHOLD_MEDIUM = float(os.getenv('RISK_THRESHOLD_MEDIUM', 0.6))
    RISK_THRESHOLD_HIGH = float(os.getenv('RISK_THRESHOLD_HIGH', 0.8))
    
    # Model management settings
    MODEL_STORAGE_PATH = os.getenv('MODEL_STORAGE_PATH', './models')
    MODEL_VERSION_RETENTION = int(os.getenv('MODEL_VERSION_RETENTION', 5))
    
    # API settings
    API_ENABLED = os.getenv('API_ENABLED', 'False').lower() == 'true'
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 8080))
    API_WORKERS = int(os.getenv('API_WORKERS', 1))
    
    # Email settings for notifications
    EMAIL_ENABLED = os.getenv('EMAIL_ENABLED', 'False').lower() == 'true'
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    EMAIL_FROM = os.getenv('EMAIL_FROM', 'noreply@financial-risk-system.com')
    
    # Backup settings
    BACKUP_ENABLED = os.getenv('BACKUP_ENABLED', 'True').lower() == 'true'
    BACKUP_INTERVAL = int(os.getenv('BACKUP_INTERVAL', 86400))  # 24 hours
    BACKUP_RETENTION_DAYS = int(os.getenv('BACKUP_RETENTION_DAYS', 30))
    BACKUP_PATH = os.getenv('BACKUP_PATH', './backups')

class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    DB_TYPE = 'sqlite'
    API_ENABLED = True

class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    DB_TYPE = 'postgres'
    API_ENABLED = True
    
    # Enhanced security for production
    PASSWORD_MIN_LENGTH = 12
    SESSION_TIMEOUT = 1800  # 30 minutes
    MAX_LOGIN_ATTEMPTS = 5

class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    DEBUG = True
    DB_TYPE = 'sqlite'
    DB_NAME = ':memory:'  # In-memory database for testing
    LOG_LEVEL = 'DEBUG'

# Configuration factory
def get_config() -> Config:
    """
    Get configuration based on environment
    """
    env = os.getenv('FLASK_ENV', 'development').lower()
    
    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }
    
    return config_map.get(env, DevelopmentConfig)()

# Initialize configuration
current_config = get_config()

def load_yaml_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from YAML file
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        logging.warning(f"Configuration file {config_path} not found")
        return {}
    except yaml.YAMLError as e:
        logging.error(f"Error parsing YAML configuration: {e}")
        return {}

def validate_config(config: Config) -> bool:
    """
    Validate configuration settings
    """
    errors = []
    
    # Validate database settings
    if config.DB_TYPE not in ['sqlite', 'postgres']:
        errors.append("DB_TYPE must be 'sqlite' or 'postgres'")
    
    # Validate security settings
    if len(config.SECRET_KEY) < 32:
        errors.append("SECRET_KEY should be at least 32 characters long")
    
    if config.PASSWORD_MIN_LENGTH < 8:
        errors.append("PASSWORD_MIN_LENGTH should be at least 8")
    
    # Validate risk thresholds
    thresholds = [config.RISK_THRESHOLD_LOW, config.RISK_THRESHOLD_MEDIUM, config.RISK_THRESHOLD_HIGH]
    if not all(0 <= t <= 1 for t in thresholds):
        errors.append("Risk thresholds must be between 0 and 1")
    
    if not (thresholds[0] < thresholds[1] < thresholds[2]):
        errors.append("Risk thresholds must be in ascending order")
    
    if errors:
        for error in errors:
            logging.error(f"Configuration validation error: {error}")
        return False
    
    return True

# Validate current configuration
if not validate_config(current_config):
    logging.error("Configuration validation failed. Please check your settings.")
    
# Export commonly used settings for backward compatibility
APP_TITLE = current_config.APP_TITLE
APP_VERSION = current_config.APP_VERSION
LOGIN_WINDOW_SIZE = current_config.LOGIN_WINDOW_SIZE
USER_INFO_WINDOW_SIZE = current_config.USER_INFO_WINDOW_SIZE
ADMIN_WINDOW_SIZE = current_config.ADMIN_WINDOW_SIZE
ROLES = current_config.ROLES
DB_NAME = current_config.DB_NAME
