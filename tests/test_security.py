"""
Tests for security utilities
"""
import pytest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'project code'))

from Client.utils.security import (
    PasswordManager, InputValidator, SessionManager, 
    hash_password, verify_password, validate_input, sanitize_input
)


class TestPasswordManager:
    """Test password management functionality"""
    
    def test_password_hashing(self):
        """Test password hashing and verification"""
        password = "TestPassword123!"
        hashed = hash_password(password)
        
        assert hashed != password
        assert verify_password(password, hashed)
        assert not verify_password("wrong_password", hashed)
    
    def test_password_strength_validation(self):
        """Test password strength validation"""
        # Strong password
        strong_password = "StrongP@ssw0rd123!"
        result = PasswordManager.validate_password_strength(strong_password)
        assert result['valid']
        assert result['score'] == 100
        
        # Weak password
        weak_password = "weak"
        result = PasswordManager.validate_password_strength(weak_password)
        assert not result['valid']
        assert result['score'] < 60
        
        # Common password
        common_password = "password"
        result = PasswordManager.validate_password_strength(common_password)
        assert not result['valid']
        assert result['score'] == 0
    
    def test_secure_password_generation(self):
        """Test secure password generation"""
        password = PasswordManager.generate_secure_password(16)
        assert len(password) == 16
        
        # Generated password should be strong
        result = PasswordManager.validate_password_strength(password)
        assert result['valid']


class TestInputValidator:
    """Test input validation functionality"""
    
    def test_username_validation(self):
        """Test username validation"""
        # Valid usernames
        assert validate_input('username', 'valid_user')['valid']
        assert validate_input('username', 'user123')['valid']
        
        # Invalid usernames
        assert not validate_input('username', 'ab')['valid']  # Too short
        assert not validate_input('username', 'user@domain')['valid']  # Special chars
        assert not validate_input('username', '')['valid']  # Empty
    
    def test_email_validation(self):
        """Test email validation"""
        # Valid emails
        assert validate_input('email', 'test@example.com')['valid']
        assert validate_input('email', 'user.name+tag@domain.co.uk')['valid']
        
        # Invalid emails
        assert not validate_input('email', 'invalid-email')['valid']
        assert not validate_input('email', '@domain.com')['valid']
        assert not validate_input('email', 'user@')['valid']
    
    def test_financial_amount_validation(self):
        """Test financial amount validation"""
        # Valid amounts
        result = validate_input('amount', '100.50')
        assert result['valid']
        assert result['value'] == 100.50
        
        result = validate_input('amount', '$1,234.56')
        assert result['valid']
        assert result['value'] == 1234.56
        
        # Invalid amounts
        assert not validate_input('amount', '-100')['valid']  # Negative
        assert not validate_input('amount', 'not_a_number')['valid']  # Invalid format
    
    def test_input_sanitization(self):
        """Test input sanitization"""
        # SQL injection attempt
        malicious_input = "'; DROP TABLE users; --"
        sanitized = sanitize_input(malicious_input)
        assert "DROP TABLE" not in sanitized
        assert ";" not in sanitized
        assert "--" not in sanitized
        
        # XSS attempt
        xss_input = "<script>alert('xss')</script>"
        sanitized = sanitize_input(xss_input)
        assert "<script>" not in sanitized.lower()
        assert "</script>" not in sanitized.lower()


class TestSessionManager:
    """Test session management functionality"""
    
    def setUp(self):
        """Set up test session manager"""
        self.session_manager = SessionManager()
    
    def test_session_creation(self):
        """Test session creation"""
        session_manager = SessionManager()
        session_id = session_manager.create_session('1', 'test_user', False)
        
        assert session_id is not None
        assert len(session_id) == 36  # UUID format
        
        # Validate session
        session_data = session_manager.validate_session(session_id)
        assert session_data is not None
        assert session_data['username'] == 'test_user'
        assert session_data['user_id'] == '1'
        assert not session_data['is_admin']
    
    def test_session_validation(self):
        """Test session validation"""
        session_manager = SessionManager()
        session_id = session_manager.create_session('1', 'test_user', False)
        
        # Valid session
        assert session_manager.validate_session(session_id) is not None
        
        # Invalid session
        assert session_manager.validate_session('invalid_session') is None
    
    def test_session_destruction(self):
        """Test session destruction"""
        session_manager = SessionManager()
        session_id = session_manager.create_session('1', 'test_user', False)
        
        # Destroy session
        assert session_manager.destroy_session(session_id)
        
        # Session should no longer be valid
        assert session_manager.validate_session(session_id) is None
        
        # Destroying non-existent session should return False
        assert not session_manager.destroy_session('non_existent')
    
    def test_login_attempts_tracking(self):
        """Test login attempts tracking"""
        session_manager = SessionManager()
        username = 'test_user'
        
        # Should allow login initially
        assert session_manager.check_login_attempts(username)
        
        # Record failed attempts
        for _ in range(3):  # Assuming max attempts is 3
            session_manager.record_login_attempt(username, False)
        
        # Should block further attempts
        assert not session_manager.check_login_attempts(username)
        
        # Successful login should reset attempts
        session_manager.record_login_attempt(username, True)
        assert session_manager.check_login_attempts(username)


if __name__ == '__main__':
    pytest.main([__file__]) 