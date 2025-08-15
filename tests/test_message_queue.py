# Unit tests for the message queue functionality
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import json
from app.services.message_queue import MessageQueueClient

# Create a simple mock settings object
class MockSettings:
    RABBITMQ_URL = 'amqp://test'

@pytest.mark.asyncio
async def test_message_queue_client_publish_user_created_event():
    """Test that the message queue client can publish UserCreated events."""
    with patch('aiormq.connect') as mock_connect, \
         patch('app.services.message_queue.settings', MockSettings()):
        # Mock the connection and channel
        mock_connection = AsyncMock()
        mock_channel = AsyncMock()
        mock_connect.return_value = mock_connection
        mock_connection.channel.return_value = mock_channel
        
        # Create the client and connect
        client = MessageQueueClient()
        await client.connect()
        
        # Test data
        user_data = {
            "id": 1,
            "username": "testuser",
            "email": "test@example.com"
        }
        
        # Publish an event
        await client.publish_user_created_event(user_data)
        
        # Verify that the message was published
        mock_channel.basic_publish.assert_called_once()
        call_args = mock_channel.basic_publish.call_args
        assert call_args[1]['routing_key'] == "user_events"
        
        # Check the message content
        published_message = json.loads(call_args[1]['body'].decode())
        assert published_message["event_type"] == "UserCreated"
        assert published_message["user_id"] == 1
        assert published_message["username"] == "testuser"
        assert published_message["email"] == "test@example.com"

@pytest.mark.asyncio
async def test_message_queue_client_handles_connection_failure():
    """Test that the message queue client handles connection failures gracefully."""
    with patch('aiormq.connect', side_effect=Exception("Connection failed")), \
         patch('app.services.message_queue.settings', MockSettings()):
        # Create the client and try to connect
        client = MessageQueueClient()
        await client.connect()
        
        # Verify that the client handles the failure gracefully
        assert client.connection is None
        assert client.channel is None
        
        # Test that publishing doesn't crash even when not connected
        user_data = {"id": 1, "username": "testuser", "email": "test@example.com"}
        # This should not raise an exception
        await client.publish_user_created_event(user_data)