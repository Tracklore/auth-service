# Unit tests for the authentication service
import pytest
from unittest.mock import AsyncMock, patch
from app.utils.security import (
    hash_password, 
    verify_password, 
    create_access_token_wrapper, 
    create_refresh_token_wrapper
)
from datetime import timedelta
from jose import jwt
from app.core.settings import settings
from app.services.auth import signup
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_password_hashing():
    """Test password hashing and verification."""
    password = "testpassword123"
    hashed = hash_password(password)
    
    # Verify that the hashed password is different from the original
    assert hashed != password
    
    # Verify that the password can be verified
    assert verify_password(password, hashed)
    
    # Verify that an incorrect password fails verification
    assert not verify_password("wrongpassword", hashed)

@pytest.mark.asyncio
async def test_access_token_creation():
    """Test access token creation."""
    data = {"sub": "testuser", "user_id": 1}
    token = create_access_token_wrapper(data)
    
    # Decode the token to verify its contents
    decoded = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    
    # Verify the token contains the expected data
    assert decoded["sub"] == "testuser"
    assert decoded["user_id"] == 1
    assert "exp" in decoded

@pytest.mark.asyncio
async def test_refresh_token_creation():
    """Test refresh token creation."""
    data = {"sub": "testuser", "user_id": 1}
    token = create_refresh_token_wrapper(data)
    
    # Decode the token to verify its contents
    decoded = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    
    # Verify the token contains the expected data
    assert decoded["sub"] == "testuser"
    assert decoded["user_id"] == 1
    assert "exp" in decoded

@pytest.mark.asyncio
async def test_token_expiration():
    """Test token expiration."""
    data = {"sub": "testuser", "user_id": 1}
    expires = timedelta(minutes=30)
    
    # Create tokens with custom expiration
    access_token = create_access_token_wrapper(data, expires)
    refresh_token = create_refresh_token_wrapper(data, expires)
    
    # Decode tokens
    access_decoded = jwt.decode(access_token, settings.secret_key, algorithms=[settings.algorithm])
    refresh_decoded = jwt.decode(refresh_token, settings.secret_key, algorithms=[settings.algorithm])
    
    # Verify expiration is set
    assert "exp" in access_decoded
    assert "exp" in refresh_decoded

@pytest.mark.asyncio
async def test_signup_publishes_user_created_event():
    """Test that signup publishes a UserCreated event to the message queue."""
    # Mock the database session and CRUD functions
    with patch('app.services.auth.get_user_by_username') as mock_get_by_username, \
         patch('app.services.auth.get_user_by_email') as mock_get_by_email, \
         patch('app.services.auth.create_user') as mock_create_user, \
         patch('app.services.auth.message_queue_client') as mock_mq_client:
        
        # Configure mocks
        mock_get_by_username.return_value = None
        mock_get_by_email.return_value = None
        
        # Mock user object
        mock_user = AsyncMock()
        mock_user.id = 1
        mock_user.username = "testuser"
        mock_user.email = "test@example.com"
        mock_user.is_active = True
        mock_user.hashed_password = "hashed_password"
        
        mock_create_user.return_value = mock_user
        
        # Mock the message queue client
        mock_mq_client.publish_user_created_event = AsyncMock()
        
        # Create a mock database session
        mock_db = AsyncMock(spec=AsyncSession)
        
        # Call the signup function
        result = await signup(mock_db, "testuser", "test@example.com", "password123")
        
        # Verify the result
        assert result.id == 1
        assert result.username == "testuser"
        assert result.email == "test@example.com"
        assert result.is_active == True
        
        # Verify that the user was created
        mock_create_user.assert_called_once_with(mock_db, "testuser", "test@example.com", "password123")
        
        # Verify that the UserCreated event was published
        mock_mq_client.publish_user_created_event.assert_called_once()
        call_args = mock_mq_client.publish_user_created_event.call_args[0][0]
        assert call_args["id"] == 1
        assert call_args["username"] == "testuser"
        assert call_args["email"] == "test@example.com"