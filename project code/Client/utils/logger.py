"""
Professional logging system for Financial Risk Assessment System
Provides structured logging with multiple outputs and security features
"""
import os
import sys
import logging
import logging.handlers
from datetime import datetime
from typing import Optional, Dict, Any
import json
import traceback

# Try to import enhanced dependencies, fall back to basics if not available
try:
    from loguru import logger
    HAS_LOGURU = True
except ImportError:
    HAS_LOGURU = False
    logger = logging.getLogger(__name__)

try:
    from config.settings import current_config
except ImportError:
    # Fallback for when config is not available
    class MockConfig:
        LOG_LEVEL = 'INFO'
        LOG_FILE = 'financial_risk_system.log'
        LOG_MAX_SIZE = 10485760  # 10MB
        LOG_BACKUP_COUNT = 5
    current_config = MockConfig()


class SecurityFilter(logging.Filter):
    """Filter to remove sensitive information from logs"""
    
    SENSITIVE_KEYS = ['password', 'secret', 'token', 'key', 'auth', 'credential']
    
    def filter(self, record):
        """Filter out sensitive information from log records"""
        if hasattr(record, 'msg') and isinstance(record.msg, str):
            for key in self.SENSITIVE_KEYS:
                if key.lower() in record.msg.lower():
                    record.msg = record.msg.replace(record.msg, '[SENSITIVE DATA FILTERED]')
        return True


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging"""
    
    def format(self, record):
        """Format log record as JSON"""
        log_data = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Add exception information if present
        if record.exc_info:
            log_data['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': traceback.format_exception(*record.exc_info)
            }
        
        # Add extra fields if present
        if hasattr(record, 'user_id'):
            log_data['user_id'] = record.user_id
        if hasattr(record, 'session_id'):
            log_data['session_id'] = record.session_id
        if hasattr(record, 'action'):
            log_data['action'] = record.action
        
        return json.dumps(log_data, ensure_ascii=False)


class AuditLogger:
    """Specialized logger for audit trails"""
    
    def __init__(self, name: str = 'audit'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Create audit log handler
        handler = logging.handlers.RotatingFileHandler(
            'audit.log',
            maxBytes=current_config.LOG_MAX_SIZE,
            backupCount=current_config.LOG_BACKUP_COUNT,
            encoding='utf-8'
        )
        
        handler.setFormatter(JSONFormatter())
        self.logger.addHandler(handler)
    
    def log_user_action(self, user_id: str, action: str, details: str = '', 
                       session_id: Optional[str] = None):
        """Log user actions for audit purposes"""
        extra = {
            'user_id': user_id,
            'action': action,
            'session_id': session_id or 'unknown'
        }
        self.logger.info(f"User action: {action} - {details}", extra=extra)
    
    def log_security_event(self, event_type: str, details: str, severity: str = 'INFO'):
        """Log security-related events"""
        extra = {'event_type': event_type, 'security': True}
        
        if severity.upper() == 'CRITICAL':
            self.logger.critical(f"Security event: {event_type} - {details}", extra=extra)
        elif severity.upper() == 'WARNING':
            self.logger.warning(f"Security event: {event_type} - {details}", extra=extra)
        else:
            self.logger.info(f"Security event: {event_type} - {details}", extra=extra)


class LoggerManager:
    """Central logger management system"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggerManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.setup_logging()
            self._initialized = True
    
    def setup_logging(self):
        """Initialize the logging system"""
        if HAS_LOGURU:
            self.setup_loguru_logging()
        else:
            self.setup_standard_logging()
        
        # Initialize audit logger
        self.audit_logger = AuditLogger()
        
        print("Logging system initialized successfully")
    
    def setup_loguru_logging(self):
        """Setup enhanced logging with loguru"""
        # Configure loguru
        logger.remove()  # Remove default handler
        
        # Console handler with colors
        logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                   "<level>{level: <8}</level> | "
                   "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                   "<level>{message}</level>",
            level=current_config.LOG_LEVEL,
            colorize=True
        )
        
        # File handler with rotation
        logger.add(
            current_config.LOG_FILE,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
            level=current_config.LOG_LEVEL,
            rotation=f"{current_config.LOG_MAX_SIZE // 1024 // 1024} MB",
            retention=f"{current_config.LOG_BACKUP_COUNT} days",
            compression="zip",
            encoding="utf-8"
        )
        
        # Error-only file
        logger.add(
            "errors.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
            level="ERROR",
            rotation="1 week",
            retention="1 month",
            encoding="utf-8"
        )
        
        logger.info("Enhanced logging system initialized with loguru")
    
    def setup_standard_logging(self):
        """Setup standard Python logging"""
        # Get root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, current_config.LOG_LEVEL))
        
        # Remove existing handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, current_config.LOG_LEVEL))
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        console_handler.addFilter(SecurityFilter())
        
        # File handler with rotation
        try:
            file_handler = logging.handlers.RotatingFileHandler(
                current_config.LOG_FILE,
                maxBytes=current_config.LOG_MAX_SIZE,
                backupCount=current_config.LOG_BACKUP_COUNT,
                encoding='utf-8'
            )
            file_handler.setLevel(logging.INFO)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            file_handler.addFilter(SecurityFilter())
            
            # Add handlers to root logger
            root_logger.addHandler(file_handler)
        except Exception as e:
            print(f"Warning: Could not setup file logging: {e}")
        
        root_logger.addHandler(console_handler)
        logging.info("Standard logging system initialized")
    
    def get_logger(self, name: str):
        """Get a logger instance with the specified name"""
        if HAS_LOGURU:
            return logger.bind(name=name)
        else:
            return logging.getLogger(name)
    
    def get_audit_logger(self) -> AuditLogger:
        """Get the audit logger instance"""
        return self.audit_logger


# Initialize the logger manager safely
try:
    logger_manager = LoggerManager()
except Exception as e:
    print(f"Warning: Could not initialize logger manager: {e}")
    logger_manager = None


# Convenience functions
def get_logger(name: str = __name__):
    """Get a logger instance"""
    if logger_manager:
        return logger_manager.get_logger(name)
    else:
        return logging.getLogger(name)


def get_audit_logger():
    """Get the audit logger"""
    if logger_manager:
        return logger_manager.get_audit_logger()
    else:
        # Return a basic logger if audit logger is not available
        return logging.getLogger('audit')


def log_exception(exc: Exception, context: str = ''):
    """Log an exception with full context"""
    if HAS_LOGURU:
        logger.error(f"Exception in {context}: {exc}", exc_info=True)
    else:
        logging.error(f"Exception in {context}: {exc}", exc_info=True)


def log_performance(func_name: str, duration: float, params: Optional[Dict[str, Any]] = None):
    """Log performance metrics"""
    message = f"Performance: {func_name} took {duration:.4f}s"
    if params:
        message += f" with params: {params}"
    
    if HAS_LOGURU:
        logger.info(message, extra={'performance': True, 'duration': duration, 'params': params})
    else:
        logging.info(message)


# Backward compatibility function
def log_action(username, action, details):
    """Helper function to log user actions (backward compatibility)."""
    try:
        audit_logger = get_audit_logger()
        if hasattr(audit_logger, 'log_user_action'):
            audit_logger.log_user_action(username, action, details)
        else:
            logging.info(f"User {username} performed {action}: {details}")
    except Exception as e:
        print(f"Warning: Could not log action: {e}")


# Example usage and testing
if __name__ == "__main__":
    # Test the logging system
    test_logger = get_logger("test")
    
    if HAS_LOGURU:
        test_logger.info("Testing enhanced logging with loguru")
        test_logger.warning("Testing warning message")
        test_logger.error("Testing error message")
    else:
        test_logger.info("Testing standard logging")
        test_logger.warning("Testing warning message")
        test_logger.error("Testing error message")
    
    try:
        audit_logger = get_audit_logger()
        if hasattr(audit_logger, 'log_user_action'):
            audit_logger.log_user_action("user123", "login", "Successful login")
            audit_logger.log_security_event("test", "System test", "INFO")
    except Exception as e:
        print(f"Could not test audit logging: {e}")
    
    try:
        raise ValueError("Test exception")
    except Exception as e:
        log_exception(e, "test_function")
    
    log_performance("test_function", 0.1234, {"param1": "value1"})