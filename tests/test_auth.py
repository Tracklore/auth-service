# Unit tests for the authentication service
import pytest
from app.utils.security import hash_password, verify_password, create_access_token, create_refresh_token
from datetime import timedelta
from jose import jwt
from app.core.settings import settings

def test_password_hashing():
    """Test password hashing and verification."""
    password = "testpassword123"
    hashed = hash_password(password)
    
    # Verify that the hashed password is different from the original
    assert hashed != password
    
    # Verify that the password can be verified
    assert verify_password(password, hashed)
    
    # Verify that an incorrect password fails verification
    assert not verify_password("wrongpassword", hashed)

def test_access_token_creation():
    """Test access token creation."""
    data = {"sub": "testuser", "user_id": 1}
    token = create_access_token(data)
    
    # Decode the token to verify its contents
    decoded = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    
    # Verify the token contains the expected data
    assert decoded["sub"] == "testuser"
    assert decoded["user_id"] == 1
    assert "exp" in decoded

def test_refresh_token_creation():
    """Test refresh token creation."""
    data = {"sub": "testuser", "user_id": 1}
    token = create_refresh_token(data)
    
    # Decode the token to verify its contents
    decoded = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    
    # Verify the token contains the expected data
    assert decoded["sub"] == "testuser"
    assert decoded["user_id"] == 1
    assert "exp" in decoded

def test_token_expiration():
    """Test token expiration."""
    data = {"sub": "testuser", "user_id": 1}
    expires = timedelta(minutes=30)
    
    # Create tokens with custom expiration
    access_token = create_access_token(data, expires)
    refresh_token = create_refresh_token(data, expires)
    
    # Decode tokens
    access_decoded = jwt.decode(access_token, settings.secret_key, algorithms=[settings.algorithm])
    refresh_decoded = jwt.decode(refresh_token, settings.secret_key, algorithms=[settings.algorithm])
    
    # Verify expiration is set
    assert "exp" in access_decoded
    assert "exp" in refresh_decoded