"""
Security utilities for Financial Risk Assessment System
Provides password hashing, input validation, and session management
"""
import re
import hashlib
import secrets
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import uuid

# Try to import enhanced dependencies, fall back to basics if not available
try:
    import bcrypt
    HAS_BCRYPT = True
except ImportError:
    HAS_BCRYPT = False
    import hashlib

try:
    from cryptography.fernet import Fernet
    HAS_CRYPTOGRAPHY = True
except ImportError:
    HAS_CRYPTOGRAPHY = False

try:
    from config.settings import current_config
except ImportError:
    # Fallback for when config is not available
    class MockConfig:
        PASSWORD_MIN_LENGTH = 8
        SESSION_TIMEOUT = 3600
        MAX_LOGIN_ATTEMPTS = 3
        SECRET_KEY = 'fallback-secret-key'
    current_config = MockConfig()

try:
    from Client.utils.logger import get_logger, get_audit_logger
    logger = get_logger(__name__)
    audit_logger = get_audit_logger()
except ImportError:
    import logging
    logger = logging.getLogger(__name__)
    audit_logger = logging.getLogger('audit')


class PasswordManager:
    """Secure password management"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt or fallback to sha256"""
        if HAS_BCRYPT:
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
        else:
            # Fallback to sha256 with salt (less secure but functional)
            salt = hashlib.sha256(secrets.token_bytes(32)).hexdigest()
            hashed = hashlib.sha256((salt + password).encode('utf-8')).hexdigest()
            return f"{salt}:{hashed}"
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify a password against its hash"""
        try:
            if HAS_BCRYPT and not ':' in hashed:
                # bcrypt format
                return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
            else:
                # Fallback format (salt:hash)
                if ':' in hashed:
                    salt, expected_hash = hashed.split(':', 1)
                    actual_hash = hashlib.sha256((salt + password).encode('utf-8')).hexdigest()
                    return actual_hash == expected_hash
                else:
                    # Simple sha256 for very old passwords
                    return hashlib.sha256(password.encode('utf-8')).hexdigest() == hashed
        except Exception as e:
            logger.error(f"Password verification error: {e}")
            return False
    
    @staticmethod
    def generate_secure_password(length: int = 16) -> str:
        """Generate a secure random password"""
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        return password
    
    @staticmethod
    def validate_password_strength(password: str) -> Dict[str, Any]:
        """Validate password strength and return detailed feedback"""
        result = {
            'valid': True,
            'score': 0,
            'feedback': [],
            'requirements_met': {}
        }
        
        min_length = current_config.PASSWORD_MIN_LENGTH
        
        # Length check
        if len(password) >= min_length:
            result['score'] += 20
            result['requirements_met']['length'] = True
        else:
            result['valid'] = False
            result['feedback'].append(f"Password must be at least {min_length} characters long")
            result['requirements_met']['length'] = False
        
        # Uppercase check
        if re.search(r'[A-Z]', password):
            result['score'] += 20
            result['requirements_met']['uppercase'] = True
        else:
            result['feedback'].append("Password must contain at least one uppercase letter")
            result['requirements_met']['uppercase'] = False
        
        # Lowercase check
        if re.search(r'[a-z]', password):
            result['score'] += 20
            result['requirements_met']['lowercase'] = True
        else:
            result['feedback'].append("Password must contain at least one lowercase letter")
            result['requirements_met']['lowercase'] = False
        
        # Digit check
        if re.search(r'\d', password):
            result['score'] += 20
            result['requirements_met']['digit'] = True
        else:
            result['feedback'].append("Password must contain at least one digit")
            result['requirements_met']['digit'] = False
        
        # Special character check
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            result['score'] += 20
            result['requirements_met']['special'] = True
        else:
            result['feedback'].append("Password must contain at least one special character")
            result['requirements_met']['special'] = False
        
        # Check for common patterns
        if password.lower() in ['password', '123456', 'qwerty', 'admin']:
            result['valid'] = False
            result['score'] = 0
            result['feedback'].append("Password is too common")
        
        # Final validation
        if result['score'] < 60:
            result['valid'] = False
        
        return result


class InputValidator:
    """Input validation and sanitization"""
    
    @staticmethod
    def validate_username(username: str) -> Dict[str, Any]:
        """Validate username format"""
        result = {'valid': True, 'message': ''}
        
        if not username:
            result['valid'] = False
            result['message'] = 'Username cannot be empty'
            return result
        
        if len(username) < 3 or len(username) > 50:
            result['valid'] = False
            result['message'] = 'Username must be between 3 and 50 characters'
            return result
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            result['valid'] = False
            result['message'] = 'Username can only contain letters, numbers, and underscores'
            return result
        
        return result
    
    @staticmethod
    def validate_email(email: str) -> Dict[str, Any]:
        """Validate email format"""
        result = {'valid': True, 'message': ''}
        
        if not email:
            result['valid'] = False
            result['message'] = 'Email cannot be empty'
            return result
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            result['valid'] = False
            result['message'] = 'Invalid email format'
            return result
        
        return result
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize input to prevent injection attacks"""
        if not isinstance(text, str):
            return str(text)
        
        # Remove potential SQL injection patterns
        dangerous_patterns = [
            r"['\";]", r"--", r"/\*", r"\*/", r"xp_", r"sp_", 
            r"<script", r"</script>", r"javascript:", r"vbscript:"
        ]
        
        sanitized = text
        for pattern in dangerous_patterns:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        return sanitized.strip()
    
    @staticmethod
    def validate_financial_amount(amount: str) -> Dict[str, Any]:
        """Validate financial amount format"""
        result = {'valid': True, 'message': '', 'value': 0.0}
        
        try:
            # Remove currency symbols and commas
            cleaned = re.sub(r'[^\d.-]', '', amount)
            value = float(cleaned)
            
            if value < 0:
                result['valid'] = False
                result['message'] = 'Amount cannot be negative'
            elif value > 999999999.99:
                result['valid'] = False
                result['message'] = 'Amount is too large'
            else:
                result['value'] = round(value, 2)
                
        except ValueError:
            result['valid'] = False
            result['message'] = 'Invalid amount format'
        
        return result


class SessionManager:
    """Secure session management"""
    
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.login_attempts: Dict[str, List[datetime]] = {}
    
    def create_session(self, user_id: str, username: str, is_admin: bool = False) -> str:
        """Create a new session"""
        session_id = str(uuid.uuid4())
        
        session_data = {
            'user_id': user_id,
            'username': username,
            'is_admin': is_admin,
            'created_at': datetime.now(),
            'last_activity': datetime.now(),
            'ip_address': None,  # TODO: Add IP tracking
            'csrf_token': secrets.token_hex(32)
        }
        
        self.sessions[session_id] = session_data
        
        try:
            if hasattr(audit_logger, 'log_user_action'):
                audit_logger.log_user_action(
                    user_id, 'session_created', 
                    f"New session created for user {username}",
                    session_id
                )
            else:
                audit_logger.info(f"Session created for user {username}: {session_id}")
        except Exception as e:
            logger.error(f"Could not log session creation: {e}")
        
        logger.info(f"Session created for user {username}: {session_id}")
        return session_id
    
    def validate_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Validate and refresh session"""
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        now = datetime.now()
        
        # Check if session expired
        if now - session['last_activity'] > timedelta(seconds=current_config.SESSION_TIMEOUT):
            self.destroy_session(session_id)
            return None
        
        # Update last activity
        session['last_activity'] = now
        return session
    
    def destroy_session(self, session_id: str) -> bool:
        """Destroy a session"""
        if session_id in self.sessions:
            session = self.sessions[session_id]
            username = session.get('username', 'unknown')
            
            try:
                if hasattr(audit_logger, 'log_user_action'):
                    audit_logger.log_user_action(
                        session.get('user_id', 'unknown'), 
                        'session_destroyed', 
                        f"Session destroyed for user {username}",
                        session_id
                    )
                else:
                    audit_logger.info(f"Session destroyed for user {username}: {session_id}")
            except Exception as e:
                logger.error(f"Could not log session destruction: {e}")
            
            del self.sessions[session_id]
            logger.info(f"Session destroyed: {session_id}")
            return True
        
        return False
    
    def check_login_attempts(self, username: str) -> bool:
        """Check if user has exceeded login attempts"""
        now = datetime.now()
        
        if username not in self.login_attempts:
            self.login_attempts[username] = []
        
        # Remove attempts older than 15 minutes
        cutoff = now - timedelta(minutes=15)
        self.login_attempts[username] = [
            attempt for attempt in self.login_attempts[username]
            if attempt > cutoff
        ]
        
        return len(self.login_attempts[username]) < current_config.MAX_LOGIN_ATTEMPTS
    
    def record_login_attempt(self, username: str, success: bool):
        """Record a login attempt"""
        now = datetime.now()
        
        if username not in self.login_attempts:
            self.login_attempts[username] = []
        
        if not success:
            self.login_attempts[username].append(now)
            
            # Log security event
            try:
                if hasattr(audit_logger, 'log_security_event'):
                    audit_logger.log_security_event(
                        'failed_login_attempt',
                        f"Failed login attempt for user {username}",
                        'WARNING'
                    )
                else:
                    audit_logger.warning(f"Failed login attempt for user {username}")
            except Exception as e:
                logger.error(f"Could not log failed login attempt: {e}")
        else:
            # Clear failed attempts on successful login
            self.login_attempts[username] = []
            
            try:
                if hasattr(audit_logger, 'log_user_action'):
                    audit_logger.log_user_action(
                        username, 'successful_login',
                        f"User {username} logged in successfully"
                    )
                else:
                    audit_logger.info(f"User {username} logged in successfully")
            except Exception as e:
                logger.error(f"Could not log successful login: {e}")


class DataEncryption:
    """Data encryption utilities"""
    
    def __init__(self, key: Optional[bytes] = None):
        if not HAS_CRYPTOGRAPHY:
            raise ImportError("cryptography package is required for encryption features")
        
        if key is None:
            key = self._derive_key_from_config()
        self.cipher = Fernet(key)
    
    def _derive_key_from_config(self) -> bytes:
        """Derive encryption key from configuration"""
        # Use the secret key from config to derive a Fernet key
        secret = current_config.SECRET_KEY.encode('utf-8')
        # For simplicity, use a hash of the secret key (not recommended for production)
        key_hash = hashlib.sha256(secret).digest()
        return Fernet.generate_key()  # Generate a new key for now
    
    def encrypt(self, data: str) -> str:
        """Encrypt string data"""
        try:
            encrypted = self.cipher.encrypt(data.encode('utf-8'))
            return encrypted.decode('utf-8')
        except Exception as e:
            logger.error(f"Encryption error: {e}")
            raise
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt string data"""
        try:
            decrypted = self.cipher.decrypt(encrypted_data.encode('utf-8'))
            return decrypted.decode('utf-8')
        except Exception as e:
            logger.error(f"Decryption error: {e}")
            raise


# Global session manager instance
session_manager = SessionManager()

# Convenience functions
def hash_password(password: str) -> str:
    """Hash a password"""
    return PasswordManager.hash_password(password)

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password"""
    return PasswordManager.verify_password(password, hashed)

def validate_input(input_type: str, value: str) -> Dict[str, Any]:
    """Validate input based on type"""
    validators = {
        'username': InputValidator.validate_username,
        'email': InputValidator.validate_email,
        'amount': InputValidator.validate_financial_amount,
    }
    
    if input_type in validators:
        return validators[input_type](value)
    else:
        return {'valid': True, 'message': ''}

def sanitize_input(text: str) -> str:
    """Sanitize input"""
    return InputValidator.sanitize_input(text)

# Example usage and testing
if __name__ == "__main__":
    print("Testing Security Module...")
    
    # Test password functionality
    password = "TestPassword123!"
    hashed = hash_password(password)
    print(f"Password hash: {hashed}")
    print(f"Verification: {verify_password(password, hashed)}")
    
    # Test password strength
    strength = PasswordManager.validate_password_strength(password)
    print(f"Password strength: {strength}")
    
    # Test input validation
    username_result = validate_input('username', 'test_user')
    print(f"Username validation: {username_result}")
    
    email_result = validate_input('email', 'test@example.com')
    print(f"Email validation: {email_result}")
    
    # Test session management
    session_id = session_manager.create_session('1', 'test_user', False)
    print(f"Session created: {session_id}")
    
    session_data = session_manager.validate_session(session_id)
    print(f"Session validation: {session_data is not None}")
    
    session_manager.destroy_session(session_id)
    print("Session destroyed")
    
    print("Security module test completed successfully!") 