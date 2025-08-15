import asyncio
import json
import aiormq
from typing import Dict, Any
from app.core.settings import settings

class MessageQueueClient:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.queue_name = "user_events"
        
    async def connect(self):
        """Connect to the message queue."""
        try:
            # Connect to RabbitMQ
            self.connection = await aiormq.connect(settings.RABBITMQ_URL)
            self.channel = await self.connection.channel()
            # Declare a queue for user events
            await self.channel.queue_declare(self.queue_name, durable=True)
        except Exception as e:
            print(f"Failed to connect to message queue: {e}")
            # We don't want to crash the service if the message queue is unavailable
            self.connection = None
            self.channel = None
    
    async def publish_user_created_event(self, user_data: Dict[str, Any]):
        """Publish a UserCreated event to the message queue."""
        # If we're not connected to the message queue, try to connect
        if not self.connection or not self.channel:
            await self.connect()
            
        # If we still can't connect, log and continue (don't block user creation)
        if not self.connection or not self.channel:
            print("Warning: Message queue not available, UserCreated event not published")
            return
            
        try:
            # Create the event payload
            event = {
                "event_type": "UserCreated",
                "user_id": user_data["id"],
                "username": user_data["username"],
                "email": user_data["email"],
                "timestamp": asyncio.get_event_loop().time()
            }
            
            # Publish the event to the queue
            await self.channel.basic_publish(
                body=json.dumps(event).encode(),
                routing_key=self.queue_name,
                properties=aiormq.spec.Basic.Properties(
                    content_type="application/json",
                    delivery_mode=2  # Make message persistent
                )
            )
            print(f"Published UserCreated event for user {user_data['id']}")
        except Exception as e:
            print(f"Failed to publish UserCreated event: {e}")
            # We don't want to block user creation if the message queue fails
            # In a production system, you might want to implement retry logic or dead letter queues

    async def close(self):
        """Close the connection to the message queue."""
        if self.connection:
            await self.connection.close()

# Global instance
message_queue_client = MessageQueueClient()